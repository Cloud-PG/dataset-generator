import random
from argparse import ArgumentTypeError

import numpy as np


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise ArgumentTypeError('Boolean value expected.')


def gen_random_files(num_files: int,
                     min_file_size: int, max_file_size: int) -> dict:
    """Generates a dict with random files with a random size."""
    sizes = []
    for size in [
        float(elm * 1024.)
        for elm in np.random.poisson(lam=4, size=num_files)
    ]:
        if size >= min_file_size and size <= max_file_size:
            sizes.append(size)
        elif size < min_file_size:
            sizes.append(min_file_size)
        else:
            sizes.append(max_file_size)

    return {
        filename: {
            'Size': sizes[filename],
            'Protocol': random.randint(0, 1)
        }
        for filename in range(num_files)
    }


def gen_fake_cpu_work(num_cpus: int = 1):
    wall_time = float(random.randint(60, 600))
    single_cpu_time = (random.random() * wall_time)
    cpu_time = float(single_cpu_time * num_cpus)
    io_time = wall_time - float((cpu_time) / num_cpus)
    return num_cpus, wall_time, cpu_time, single_cpu_time, io_time


COLUMNS = {
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
