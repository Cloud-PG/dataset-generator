import datetime
import json
from pathlib import Path, PurePath

import pandas as pd

_COLUMNS = {
    'Filename': "object",
    'SiteName': "object",
    'UserID': "int64",
    'TaskID': "int64",
    'TaskMonitorID': "object",
    'JobID': "int64",
    'Protocol': "object",
    'JobExecExitCode': "int64",
    'JobStart': "int64",
    'JobEnd': "int64",
    'NumCPU': "int64",
    'WrapWC': "float64",
    'WrapCPU': "float64",
    'Size': "float64",
    'DataType': "object",
    'FileType': "object",
    'JobLengthH': "float64",
    'JobLengthM': "float64",
    'JobSuccess': "bool",
    'CPUTime': "float64",
    'IOTime': "float64",
    'reqDay': "int64",
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

    def save(self, dest_folder: 'PurePath' = Path(".")):
        if not dest_folder.exists():
            Path.mkdir(dest_folder, parents=True)
        file_path = dest_folder.joinpath(f"dataset_{self._date}.csv.gz")
        self._df.to_csv(file_path, index=False)


class Generator(object):

    def __init__(self,
                 num_days: int = 1,
                 start_date: 'datetime.date' = datetime.date(2020, 1, 1),
                 dest_folder: 'PurePath' = Path("."),
                 ):
        self._num_days = num_days
        self._days = []
        self._start_date = start_date
        self._dest_folder = dest_folder

    @property
    def days(self):
        return self._days
    
    @property
    def num_days(self, value: int):
        return self._num_days

    @num_days.setter
    def num_days(self, value: int):
        self._num_days = value
    
    @property
    def dest_folder(self, value: int):
        return self._dest_folder
    
    @dest_folder.setter
    def dest_folder(self, dest_folder: 'PurePath' = Path("./dataset")):
        if isinstance(dest_folder, Path):
            self._dest_folder = dest_folder
        else:
            raise Exception("ERROR: destination folder is not a PurePath object...")

    def clean(self):
        del self._days[:]

    def prepare(self):
        delta = datetime.timedelta(days=1)
        cur_date = self._start_date
        for n_day in range(1, self._num_days+1):
            self._days.append(
                Day(cur_date)
            )
            cur_date = cur_date + delta
            yield int(float(n_day / self._num_days) * 100.)

    def save(self):
        for idx, day in enumerate(self._days, 1):
            day.save(self._dest_folder)
            yield int(float(idx / len(self._days) * 100.))
