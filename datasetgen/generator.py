import datetime
import importlib
import json
import shutil
import time
from pathlib import Path, PurePath

import pandas as pd

from . import functions

_COLUMNS = {
    'Filename': "int64",
    'SiteName': "int64",
    'UserID': "int64",
    'TaskID': "int64",
    'TaskMonitorID': "int64",
    'JobID': "int64",
    'Protocol': "int64",
    'JobExecExitCode': "int64",
    'JobStart': "int64",
    'JobEnd': "int64",
    'NumCPU': "int64",
    'WrapWC': "float64",
    'WrapCPU': "float64",
    'Size': "float64",
    'DataType': "int64",
    'FileType': "int64",
    'JobLengthH': "float64",
    'JobLengthM': "float64",
    'JobSuccess': "bool",
    'CPUTime': "float64",
    'IOTime': "float64",
    'reqDay': "int64",
    'Region': "int64",
    'Campain': "int64",
    'Process': "int64",
}


def _make_empty_df() -> 'pd.DataFrame':
    df = pd.DataFrame(index=None)

    for column, type_ in _COLUMNS.items():
        df[column] = pd.Series(dtype=type_)

    return df


class Day(object):

    def __init__(self, date: 'datetime.date'):
        self._date = date
        self._df = _make_empty_df()

    def __repr__(self):
        return f"{self._date}=>{self._df.to_string()}"

    @property
    def df(self):
        return self._df

    def reset_index(self):
        self._df.reset_index(drop=True, inplace=True)
        return self

    def append(self, row: dict):
        row['reqDay'] = int(time.mktime(self._date.timetuple()))
        row['JobSuccess'] = True
        self._df = self._df.append(
            pd.Series(
                [row[key] if key in row else None for key in _COLUMNS],
                index=_COLUMNS.keys()
            ),
            ignore_index=True
        )
        return self

    def save(self, dest_folder: 'PurePath' = Path(".")):
        file_path = dest_folder.joinpath(f"dataset_{self._date}.csv.gz")
        self._df.to_csv(file_path, index=False)
        return self


class Generator(object):

    def __init__(self,
                 config: dict = {},
                 num_days: int = 1,
                 num_req_x_day: int = 1000,
                 start_date: 'datetime.date' = datetime.date(2020, 1, 1),
                 dest_folder: 'PurePath' = Path("."),
                 ):
        self._start_date = start_date
        self._days = []

        for key, val in config.items():
            setattr(self, f"_{key}", val)

        self._num_days = num_days
        self._num_req_x_day = num_req_x_day
        self._dest_folder = dest_folder

    @property
    def df(self):
        return pd.concat([day.df for day in self._days])

    @property
    def days(self):
        return self._days

    @property
    def num_req_x_day(self):
        return self._num_req_x_day

    @num_req_x_day.setter
    def num_req_x_day(self, value: int):
        assert isinstance(
            value, int), "ERROR: num req x day needs an integer value"
        self._num_req_x_day = value

    @property
    def num_days(self):
        return self._num_days

    @property
    def tot_num_requests(self):
        return self._num_days * self._num_req_x_day

    @num_days.setter
    def num_days(self, value: int):
        assert isinstance(
            value, int), "ERROR: num days needs an integer value"
        self._num_days = value

    @property
    def dest_folder(self):
        return self._dest_folder

    @dest_folder.setter
    def dest_folder(self, dest_folder: 'PurePath' = Path("./dataset")):
        if isinstance(dest_folder, Path):
            self._dest_folder = dest_folder
        else:
            raise Exception(
                "ERROR: destination folder is not a PurePath object...")

    def clean(self):
        del self._days[:]

    def prepare(self, function_name, kwargs: dict):
        if function_name not in dir(functions):
            importlib.reload(functions)

        cur_gen_obj = getattr(functions, function_name)(**kwargs)
        cur_gen_obj.num_req_x_day = self._num_req_x_day
        cur_gen_fun = next(cur_gen_obj)

        delta = datetime.timedelta(days=1)
        cur_date = self._start_date

        for n_day in range(self._num_days):
            cur_day = Day(cur_date)
            cur_gen_obj.day_idx = n_day

            for n_req in range(self._num_req_x_day):
                new_row, exit_ = next(cur_gen_fun)
                cur_day.append(new_row)
                yield int(float((n_day * self._num_req_x_day + n_req) / self.tot_num_requests) * 100.)
                if exit_:
                    break

            cur_day.reset_index()

            self._days.append(
                cur_day
            )
            cur_date = cur_date + delta
            yield int(float((n_day * self._num_req_x_day + n_req) / self.tot_num_requests) * 100.)

        yield 100

    def save(self):
        if self._dest_folder.exists():
            shutil.rmtree(self._dest_folder)
        Path.mkdir(self._dest_folder, parents=True)
        for idx, day in enumerate(self._days, 1):
            day.save(self._dest_folder)
            yield int(float(idx / len(self._days) * 100.))
