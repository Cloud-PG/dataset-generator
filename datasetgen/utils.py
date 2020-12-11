import random
from argparse import ArgumentTypeError

import numpy as np

_FILE_SIZE_STEP = 100

# Use case file size distribution (bins)
_SIZE_PROB_DISTRIBUTION = np.array([
    2.32126756e-05, 2.81787018e-05, 5.16012095e-05, 3.83730445e-05,
    2.51317649e-05, 2.68803657e-05, 2.55383146e-05, 3.09471740e-04,
    3.80631050e-04, 3.41099557e-04, 3.09113277e-04, 2.77380544e-04,
    3.44028464e-04, 3.35661409e-04, 4.47847264e-04, 7.54818506e-04,
    9.63479039e-05, 1.17593404e-05, 1.46620177e-05, 1.61046133e-05,
    1.54969746e-05, 4.37281344e-05, 1.00981696e-05, 9.75282094e-06,
    2.66574191e-05, 1.72412038e-05, 1.03429737e-05, 9.59107537e-06,
    1.11429586e-05, 1.69570562e-05, 1.50423383e-05, 9.86210849e-06,
    7.49275441e-06, 8.20968074e-06, 8.23153825e-06, 7.65012848e-06,
    7.12991975e-06, 7.13866275e-06, 6.81954310e-06, 6.67091204e-06,
    5.91901369e-06, 5.50809251e-06, 5.32448942e-06, 5.10154282e-06,
    4.82613820e-06, 4.98788377e-06, 4.91356824e-06, 4.79990918e-06,
    4.68625013e-06, 3.81194974e-06, 2.78464677e-06, 2.44366961e-06,
    2.62290119e-06, 2.65787321e-06, 2.16389348e-06, 2.92453483e-06,
    4.93542575e-06, 2.53109965e-06, 2.02837692e-06, 2.02837692e-06,
    2.55732866e-06, 2.81524728e-06, 2.74530325e-06, 2.31689605e-06,
    1.70488578e-06, 1.25899257e-06, 1.15407653e-06, 1.35953712e-06,
    1.12784751e-06, 7.99984864e-07, 7.51898342e-07, 5.85781267e-07,
    5.98895773e-07, 6.07638777e-07, 1.69177127e-06, 6.88948714e-06,
    1.08413249e-06, 8.56814390e-07, 9.96702454e-07, 2.30378155e-06,
    3.72889120e-06, 5.86218417e-06, 7.65012848e-07, 5.28951741e-07,
    3.58463163e-07, 2.88519131e-07, 2.44804111e-07, 1.39888064e-07,
    5.68295259e-08, 6.12010279e-08, 2.62290119e-08, 9.61730438e-08,
    9.18015418e-08, 1.66117076e-07, 8.74300398e-08, 7.86870358e-08,
    9.18015418e-08, 1.35516562e-07, 7.86870358e-08, 9.61730438e-08,
])


def gen_random_sizes(num_files: int, min_file_size: int,
                     max_file_size: int) -> list:
    """Generates a list of sizes for each files using a random distribution.

    :param num_files: total number of files
    :type num_files: int
    :param min_file_size: minimum file size
    :type min_file_size: int
    :param max_file_size: maximum file size
    :type max_file_size: int
    :return: list of file sizes
    :rtype: list
    """
    file_sizes = list(range(min_file_size, max_file_size, _FILE_SIZE_STEP))
    file_size_prob = np.random.randint(2, size=len(file_sizes))
    for idx, size in enumerate(file_sizes):
        if size >= min_file_size and size <= max_file_size:
            file_size_prob[idx] = (
                file_size_prob[idx] + random.random() * 100.0) % 100
        elif size < min_file_size and size > min_file_size - (min_file_size / 2):
            file_size_prob[idx] = (
                file_size_prob[idx] + random.random() * 10) % 100
        elif size > max_file_size and size < max_file_size * 2 - min_file_size:
            file_size_prob[idx] = (
                file_size_prob[idx] + random.random() * 10) % 100
    file_size_prob = file_size_prob.astype(float)
    file_size_prob /= file_size_prob.sum()
    sizes = np.random.choice(file_sizes, size=num_files, p=file_size_prob)
    return sizes


def gen_in_range_random_sizes(num_files: int, min_file_size: int,
                              max_file_size: int) -> list:
    """Generates a list of sizes that follows the use case distribution.

    :param num_files: total number of files
    :type num_files: int
    :param min_file_size: minimum file size
    :type min_file_size: int
    :param max_file_size: masimum file size
    :type max_file_size: int
    :return: list of file sizes
    :rtype: list
    """
    bins = np.linspace(
        min_file_size, max_file_size, len(_SIZE_PROB_DISTRIBUTION)
    )
    prob = _SIZE_PROB_DISTRIBUTION / _SIZE_PROB_DISTRIBUTION.sum()
    sizes = np.random.choice(bins, size=num_files, p=prob)
    return sizes


def gen_random_files(num_files: int, min_file_size: int, max_file_size: int,
                     size_generator_function: str = 'gen_in_range_random_sizes',
                     start_from: int = 0,) -> dict:
    """Generates a dict with random files with a random size.

    :param num_files: total number of files
    :type num_files: int
    :param min_file_size: minimum file size
    :type min_file_size: int
    :param max_file_size: maximum file size
    :type max_file_size: int
    :param size_generator_function: function to use to generate file sizes, defaults to 'gen_in_range_random_sizes'
    :type size_generator_function: str, optional
    :param start_from: filename reference index, defaults to 0
    :type start_from: int, optional
    :raises Exception: size generator function not exists
    :return: dictionary with filenames and their sizes
    :rtype: dict
    """
    if size_generator_function == 'gen_in_range_random_sizes':
        sizes = gen_in_range_random_sizes(
            num_files, min_file_size, max_file_size
        )
    elif size_generator_function == 'gen_random_sizes':
        sizes = gen_random_sizes(num_files, min_file_size, max_file_size)
    else:
        raise Exception(
            f"ERROR: Size generator function {size_generator_function} does not exist...")

    return {
        filename: {
            'Size': sizes[filename-start_from],
            'Protocol': random.randint(0, 1)
        }
        for filename in range(start_from, start_from+num_files)
    }


def gen_fake_cpu_work(num_cpus: int = 1) -> tuple:
    """Generates a fake CPU times.

    :param num_cpus: number of CPU to simulate, defaults to 1
    :type num_cpus: int, optional
    :return: work statistics -> number of CPUs, wall time, CPU time, single CPU time and io time
    :rtype: tuple
    """
    wall_time = float(random.randint(60, 600))
    single_cpu_time = (random.random() * wall_time)
    cpu_time = float(single_cpu_time * num_cpus)
    io_time = wall_time - float((cpu_time) / num_cpus)
    return num_cpus, wall_time, cpu_time, single_cpu_time, io_time


# Dataset columns with types
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
    'Campaign': "int64",
    'Process': "int64",
}
