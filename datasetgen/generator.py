import datetime
import importlib
import random
import shutil
import time
from pathlib import Path, PurePath
from typing import List, Tuple, Generator

import numpy as np
import pandas as pd

from . import functions
from .utils import COLUMNS, gen_fake_cpu_work

_DEFAULT_SEED = 42


def _make_empty_df() -> 'pd.DataFrame':
    """Generates an empy Dataframe with che columns indicated in COLUMNS dict.

    :return: a new DataFrame
    :rtype: pd.DataFrame
    """
    df = pd.DataFrame(index=None)

    for column, type_ in COLUMNS.items():
        df[column] = pd.Series(dtype=type_)

    return df


class Day(object):

    def __init__(self, date: 'datetime.date', df: 'pd.DataFrame' = None):
        """Initialize current day basic information.

        :param date: The current date of the Day object
        :type date: datetime.date
        """
        self._date = date
        if df is not None:
            self._df = df
        else:
            self._df = _make_empty_df()

    def __repr__(self):
        return f"{self._date}=>{self._df.to_string()}"

    @property
    def df(self):
        return self._df

    def reset_index(self):
        """Reset the dataframe index inplace.

        :return: self
        :rtype: Day
        """
        self._df.reset_index(drop=True, inplace=True)
        return self

    def bulk_append(self, rows: List[dict]):
        """Insert a bunch of rows into the day's dataframe.

        For each row it sets these default value:
            - reqDay = int(time.mktime(self._date.timetuple()))
            - JobSuccess = True
            - SiteName = 0
            - DataType = 0
            - FileType = 0

        Also, if there is no information about the job this function generates
        a random fake information on cpu work using `gen_fake_cpu_work`:
            - NumCPU
            - WrapWC
            - WrapCPU
            - CPUTime
            - IOTime

        :param rows: List of rows
        :type rows: List[dict]
        :return: self
        :rtype: Day
        """
        cur_req_time = int(time.mktime(self._date.timetuple()))
        for row in rows:
            row['reqDay'] = cur_req_time
            row['JobSuccess'] = True
            row['SiteName'] = 0
            row['DataType'] = 0
            row['FileType'] = 0
            for key in row:
                if key not in [
                    'NumCPU',
                    'WrapWC',
                    'WrapCPU',
                    'CPUTime',
                    'IOTime',
                ]:
                    num_cpus, wall_time, cpu_time, single_cpu_time, io_time = gen_fake_cpu_work()
                    row['NumCPU'] = num_cpus
                    row['WrapWC'] = wall_time
                    row['WrapCPU'] = cpu_time
                    row['CPUTime'] = single_cpu_time
                    row['IOTime'] = io_time
                    break

        keys = list(rows[0].keys())
        new_df = pd.DataFrame(data={
            key: [elm[key] for elm in rows]
            for key in keys
        })
        new_df.Size *= 1024**2

        self._df = self._df.append(new_df, ignore_index=True)
        return self

    def append(self, row: dict):
        """Insert a single row into the day's dataframe.

        It sets these default value:
            - reqDay = int(time.mktime(self._date.timetuple()))
            - JobSuccess = True
            - SiteName = 0
            - DataType = 0
            - FileType = 0

        If there is no information about the job this function generates
        a random fake information on cpu work using `gen_fake_cpu_work`:
            - NumCPU
            - WrapWC
            - WrapCPU
            - CPUTime
            - IOTime

        :param row: the current row's columns
        :type row: dict
        :return: self
        :rtype: Day
        """
        row['reqDay'] = int(time.mktime(self._date.timetuple()))
        row['JobSuccess'] = True
        row['SiteName'] = 0
        row['DataType'] = 0
        row['FileType'] = 0
        row['Size'] = row['Size'] * 1024**2  # Convert to bytes

        for key in row:
            if key not in [
                'NumCPU',
                'WrapWC',
                'WrapCPU',
                'CPUTime',
                'IOTime',
            ]:
                num_cpus, wall_time, cpu_time, single_cpu_time, io_time = gen_fake_cpu_work()
                row['NumCPU'] = num_cpus
                row['WrapWC'] = wall_time
                row['WrapCPU'] = cpu_time
                row['CPUTime'] = single_cpu_time
                row['IOTime'] = io_time
                break

        self._df = self._df.append(
            pd.Series(
                [row[key] if key in row else None for key in COLUMNS],
                index=COLUMNS.keys()
            ),
            ignore_index=True
        )
        return self

    def save(self, dest_folder: 'PurePath' = Path(".")):
        """Export the current day dataframe in a zipped csv format.

        :param dest_folder: the destination directory, defaults to Path(".")
        :type dest_folder: PurePath, optional
        :return: self
        :rtype: Day
        """
        file_path = dest_folder.joinpath(f"dataset_{self._date}.csv.gz")
        self._df.to_csv(file_path, index=False)
        return self


class Generator(object):

    """The main generatore object that creates datasets."""

    def __init__(self,
                 config: dict = {},
                 num_days: int = -1,
                 num_req_x_day: int = -1,
                 start_date: 'datetime.date' = datetime.date(2020, 1, 1),
                 seed: int = _DEFAULT_SEED,
                 dest_folder: 'PurePath' = Path("."),
                 ):
        """Initialize the generator.

        :param config: A dictionary with the configuration to use, defaults to {}
        :type config: dict, optional
        :param num_days: number of days to generate, defaults to -1
        :type num_days: int, optional
        :param num_req_x_day: number of requests per day, defaults to -1
        :type num_req_x_day: int, optional
        :param start_date: the starting date of the generator data, defaults to datetime.date(2020, 1, 1)
        :type start_date: datetime, optional
        :param seed: the random generator seed, defaults to _DEFAULT_SEED
        :type seed: int, optional
        :param dest_folder: the folder where to store the dataset, defaults to Path(".")
        :type dest_folder: PurePath, optional
        """
        self._start_date = start_date
        self._days = []
        self._seed = seed

        for key, val in config.items():
            setattr(self, f"_{key}", val)

        if num_days != -1:
            self._num_days = num_days
        if num_req_x_day != -1:
            self._num_req_x_day = num_req_x_day

        self._dest_folder = dest_folder
        self.__update_seeds()

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, value: int):
        """Change seed value

        :param value: new seed value
        :type value: int
        """
        assert isinstance(value, int), "ERROR: value in not an integer"
        self._seed = value
        self.__update_seeds()

    def __update_seeds(self):
        """Initialize the random generator seeds.

        Internal Python random generator seed and NumPy random seed.
        """
        random.seed(self._seed)
        np.random.seed(self._seed)

    @property
    def df(self) -> 'pd.DataFrame':
        """Returns a new dataframes that contains all the days' dataframes.

        :return: the concatenated dataframe
        :rtype: pd.DataFrame
        """
        if not self._days:
            return None

        all_df = pd.concat([day.df for day in self._days])
        all_df['Date'] = pd.to_datetime(all_df.reqDay, unit='s')
        return all_df

    @property
    def df_stats(self) -> Tuple['pd.DataFrame']:
        """Returns the concat days' dataframes and some useful stats

        :return: a tuple with several DataFrames
        :rtype: Tuple[pd.DataFrame]
        """
        if not self._days:
            return (None, None, None, None, None, None)

        df = self.df

        file_frequencies = df.Filename.value_counts().reset_index()
        file_frequencies.rename(
            columns={'Filename': "# requests", 'index': "Filename"},
            inplace=True
        )

        all_day_file_size = {'day': [], 'Size': []}
        for idx, group in df.groupby('reqDay')[['Filename', 'Size']]:
            all_day_file_size['day'].append(pd.to_datetime(idx, unit="s"))
            all_day_file_size['Size'].append(
                group.drop_duplicates('Filename').Size.sum() / 1024**2
            )
        all_day_file_size = pd.DataFrame(data=all_day_file_size)

        num_files = df.groupby('reqDay').Filename.nunique()
        num_files = num_files.reset_index()
        num_files['day'] = pd.to_datetime(num_files.reqDay, unit="s")
        num_files.rename(
            columns={'Filename': "numFiles"},
            inplace=True
        )

        num_req = df.groupby('reqDay').size()
        num_req = num_req.reset_index()
        num_req.rename(
            columns={0: 'numReq'},
            inplace=True
        )
        num_req['day'] = pd.to_datetime(num_req.reqDay, unit="s")

        file_sizes = df[['Filename', 'Size']].copy()
        file_sizes.drop_duplicates("Filename", inplace=True)
        file_sizes.Size /= 1024**2

        return (df, file_frequencies, all_day_file_size,
                file_sizes, num_files, num_req)

    @property
    def days(self) -> List['pd.DataFrame']:
        """Returns a list of days' DataFrames.

        :return: a list with days' DataFrames
        :rtype: List[pd.DataFrame]
        """
        return self._days

    @property
    def num_req_x_day(self):
        return self._num_req_x_day

    @num_req_x_day.setter
    def num_req_x_day(self, value: int):
        """Set the number of requests per day.

        :param value: number of requests
        :type value: int
        """
        assert isinstance(
            value, int), "ERROR: num req x day needs an integer value"
        self._num_req_x_day = value

    @property
    def num_days(self) -> int:
        return self._num_days

    @property
    def tot_num_requests(self) -> int:
        return self._num_days * self._num_req_x_day

    @num_days.setter
    def num_days(self, value: int):
        """Set the number of days to generate.

        :param value: number of days
        :type value: int
        """
        assert isinstance(
            value, int), "ERROR: num days needs an integer value"
        self._num_days = value

    @property
    def dest_folder(self) -> PurePath:
        return self._dest_folder

    @dest_folder.setter
    def dest_folder(self, dest_folder: 'PurePath' = Path("./dataset")):
        """Change the destination folder

        :param dest_folder: path of destination folder, defaults to Path("./dataset")
        :type dest_folder: PurPath, optional
        :raises Exception: When folder is not a PurePath object
        """
        if isinstance(dest_folder, Path):
            self._dest_folder = dest_folder
        else:
            raise Exception(
                "ERROR: destination folder is not a PurePath object...")

    def clean(self):
        """Delete all day dataframes.
        """
        del self._days[:]

    def prepare(self, function_name: str, kwargs: dict,
                max_buf_len: int = 1024) -> Generator[int, None, None]:
        """Prepare the dataset.

        This method recall the function generators.

        :param function_name: The function to use during the preparation
        :type function_name: str
        :param kwargs: arguments of generator function
        :type kwargs: dict
        :param max_buf_len: size of row buffer, defaults to 1024
        :type max_buf_len: int, optional
        :yield: status percentage of the preparation
        :rtype: int
        """
        if function_name not in dir(functions):
            importlib.reload(functions)

        cur_gen_obj = getattr(functions, function_name)(**kwargs)
        cur_gen_obj.num_req_x_day = self._num_req_x_day

        delta = datetime.timedelta(days=1)
        cur_date = self._start_date

        buffer = []

        for n_day in range(self._num_days):
            cur_day = Day(cur_date)
            cur_gen_obj.day_idx = n_day

            for n_req, (elm, percentage) in enumerate(
                cur_gen_obj.gen_day_elements(self._num_req_x_day)
            ):
                # Old method with low performaces
                # cur_day.append(elm)

                buffer.append(elm)

                if len(buffer) == 100:
                    cur_day.bulk_append(buffer)
                    del buffer[:]
                    buffer = []

                if percentage is None:
                    yield int(
                        float(
                            (n_day * self._num_req_x_day + n_req) /
                            self.tot_num_requests
                        ) * 100.)
                else:
                    yield int(
                        (percentage + (n_day * 100.)) /
                        (self._num_days * 100.) * 100.
                    )
            else:
                if len(buffer) != 0:
                    cur_day.bulk_append(buffer)

            cur_day.reset_index()

            self._days.append(
                cur_day
            )
            cur_date = cur_date + delta

        yield 100

    def _open_dataset_file(self, filename: 'str') -> 'Day':
        """Open a single dataset day.

        :return: the current day data
        :rtype: Day
        """
        cur_date = [
            int(elm)
            for elm in filename.as_posix().rsplit(
                "_", 1)[1].split(
                    ".", 1)[0].split(
                        "-")
        ]
        cur_date = datetime.date(*cur_date)
        df = pd.read_csv(Path(filename))
        return Day(cur_date, df)

    def open_data(self, folder: str):
        """Open dataset from a folder.

        :param folder: the dataset folder
        :type folder: str
        """
        del self._days[:]
        self._days = []
        for file_ in Path(folder).resolve().glob("*.csv*"):
            self._days.append(
                self._open_dataset_file(file_)
            )

    def save(self):
        """Exports all days' DataFrames in dest_folder."""
        if self._dest_folder.exists():
            shutil.rmtree(self._dest_folder)
        Path.mkdir(self._dest_folder, parents=True)
        for idx, day in enumerate(self._days, 1):
            day.save(self._dest_folder)
            yield int(float(idx / len(self._days) * 100.))
