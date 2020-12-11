import random

from numpy import random as np_random
from typing import Generator

from .utils import gen_fake_cpu_work, gen_random_files


class GenFunction(object):

    def __init__(self):
        self._day_idx = -1
        self._num_req_x_day = -1

    @property
    def day_idx(self):
        return self.day_idx

    @day_idx.setter
    def day_idx(self, value: int):
        """Set the index of the current day.

        Usually set by the Generator object to indicate 
        the current day sequence.

        :param value: current day index
        :type value: int
        :return: self
        :rtype: GenFunction
        """
        self._day_idx = value
        return self

    @property
    def num_req_x_day(self):
        return self.num_req_x_day

    @num_req_x_day.setter
    def num_req_x_day(self, value: int):
        """Set the number of requests per day.

        :param value: number of requests
        :type value: int
        :return: self
        :rtype: GenFunction
        """
        self._num_req_x_day = value
        return self

    def gen_day_elements(self, max_num: int = -1) -> Generator[int, None, None]:
        """Generates all the day's entries.

        :param max_num: maximum number of requests, defaults to -1
        :type max_num: int, optional
        :yield: the percentage of work done
        :rtype: Generator[int, None, None]
        """
        raise NotImplementedError

    @property
    def name(self):
        return repr(self)


class RandomGenerator(GenFunction):

    def __init__(self, num_files: int, min_file_size: int, max_file_size: int,
                 size_generator_function: str):
        """Initialize the random function parameters.

        :param num_files: total number of files
        :type num_files: int
        :param min_file_size: minumum size of the files
        :type min_file_size: int
        :param max_file_size: maximum size of the files
        :type max_file_size: int
        :param size_generator_function: name of the size generator function
        :type size_generator_function: str
        """
        super().__init__()
        self._num_files: int = num_files
        self._min_file_size: int = min_file_size
        self._max_file_size: int = max_file_size
        self._size_generator_function: str = size_generator_function

        self._files = gen_random_files(
            num_files, min_file_size, max_file_size, size_generator_function
        )

    def __repr__(self):
        return "Random Generator"

    def gen_day_elements(self, max_num: int = -1) -> Generator[int, None, None]:
        """Generates all the day's entries.

        :param max_num: maximum number of requests, defaults to -1
        :type max_num: int, optional
        :yield: the percentage of work done
        :rtype: Generator[int, None, None]
        """
        filenames: list = list(self._files.keys())
        for _ in range(max_num):
            cur_file = random.choice(filenames)
            yield {
                'Filename': cur_file,
                'Size': self._files[cur_file]['Size'],
                'Protocol': self._files[cur_file]['Protocol'],
            }, None


class HighFrequencyDataset(GenFunction):

    """Dataset to test the frequency aspect."""

    def __init__(self, num_files: int, min_file_size: int, max_file_size: int,
                 lambda_less_req_files: float, lambda_more_req_files: float,
                 perc_more_req_files: float, perc_files_x_day: float,
                 size_generator_function: str):
        """Initialize the frequency function parameters.

        :param num_files: total number of files
        :type num_files: int
        :param min_file_size: minumum size of the files
        :type min_file_size: int
        :param max_file_size: maximum size of the files
        :type max_file_size: int
        :param lambda_less_req_files: Poisson distribution lambda for less requested files
        :type lambda_less_req_files: float
        :param lambda_more_req_files: Poisson distribution lambda for more requested files
        :type lambda_more_req_files: float
        :param perc_more_req_files: percentage of more requested files
        :type perc_more_req_files: float
        :param perc_files_x_day: percentage of files per day (selected files)
        :type perc_files_x_day: float
        :param size_generator_function: name of the size generator function
        :type size_generator_function: str
        """
        super().__init__()
        self._num_files: int = num_files
        self._min_file_size: int = min_file_size
        self._max_file_size: int = max_file_size
        self._lambda_less_req_files: float = lambda_less_req_files
        self._lambda_more_req_files: float = lambda_more_req_files
        self._perc_more_req_files: float = perc_more_req_files
        self._perc_files_x_day: float = perc_files_x_day
        self._size_generator_function: str = size_generator_function

        self._num_more_req_files = int(
            (num_files / 100.) * perc_more_req_files)
        self._num_less_req_files = num_files - self._num_more_req_files

        self._more_req_files = gen_random_files(
            self._num_more_req_files, min_file_size, max_file_size,
            size_generator_function
        )
        self._less_req_files = gen_random_files(
            self._num_less_req_files, min_file_size, max_file_size,
            size_generator_function,
            start_from=self._num_more_req_files,
        )

        assert len(set(self._more_req_files.keys()) &
                   set(self._less_req_files.keys())) == 0

        self._more_req_files_freq = {
            filename: freq
            for filename, freq in enumerate(
                np_random.poisson(
                    lam=self._lambda_more_req_files,
                    size=self._num_more_req_files,
                )
            )
        }

        self._less_req_files_freq = {
            filename: freq
            for filename, freq in enumerate(
                np_random.poisson(
                    lam=self._lambda_less_req_files,
                    size=self._num_less_req_files,
                ),
                self._num_more_req_files
            )
        }

    def __repr__(self):
        return "High Frequency Dataset"

    def gen_day_elements(self, max_num: int = -1) -> Generator:
        """Generates all the day's entries.

        :param max_num: maximum number of requests, defaults to -1
        :type max_num: int, optional
        :yield: the percentage of work done
        :rtype: Generator[int, None, None]
        """

        file_perc_x_day = self._perc_files_x_day / 100.
        filenames = list(self._more_req_files.keys()) + \
            list(self._less_req_files.keys())
        num_visible_files = int(len(filenames) * file_perc_x_day)

        random.shuffle(filenames)
        filenames = filenames[:num_visible_files]

        all_requests = []

        for cur_file in filenames:
            if cur_file in self._more_req_files_freq:
                max_num_req = self._more_req_files_freq[cur_file]
                file_info = self._more_req_files[cur_file]
            elif cur_file in self._less_req_files_freq:
                max_num_req = self._less_req_files_freq[cur_file]
                file_info = self._less_req_files[cur_file]
            for _ in range(random.randint(0, max_num_req)):
                all_requests.append({
                    'Filename': cur_file,
                    **file_info.copy(),
                })

        random.shuffle(all_requests)

        for num, elm in enumerate(all_requests):
            yield elm, float(num / len(all_requests)) * 100.


class RecencyFocusedDataset(GenFunction):

    """Dataset to test the recency aspect."""

    def __init__(self, num_files: int, min_file_size: int, max_file_size: int,
                 perc_files_x_day: float, size_generator_function: str):
        """Initialize the recency function parameters.

        :param num_files: total number of files
        :type num_files: int
        :param min_file_size: minumum size of the files
        :type min_file_size: int
        :param max_file_size: maximum size of the files
        :type max_file_size: int
        :param perc_files_x_day: percentage of files per day (selected files)
        :type perc_files_x_day: float
        :param size_generator_function: name of the size generator function
        :type size_generator_function: str
        """
        super().__init__()
        self._num_files: int = num_files
        self._min_file_size: int = min_file_size
        self._max_file_size: int = max_file_size
        self._perc_files_x_day: float = perc_files_x_day
        self._size_generator_function: str = size_generator_function

        self._files = gen_random_files(
            num_files, min_file_size, max_file_size,
            size_generator_function
        )

    def __repr__(self):
        return "Recency Focused Dataset"

    def gen_day_elements(self, max_num: int = -1) -> Generator:
        """Generates all the day's entries.

        :param max_num: maximum number of requests, defaults to -1
        :type max_num: int, optional
        :yield: the percentage of work done
        :rtype: Generator[int, None, None]
        """
        all_requests = []
        file_perc_x_day = self._perc_files_x_day / 100.

        filenames = list(self._files.keys())
        num_visible_files = int(len(self._files) * file_perc_x_day)

        random.shuffle(filenames)
        filenames = filenames[:num_visible_files]

        while len(all_requests) < max_num:
            for cur_file in filenames:
                file_info = self._files[cur_file]
                all_requests.append({
                    'Filename': cur_file,
                    **file_info.copy(),
                })
                if len(all_requests) == max_num:
                    break

            if random.random() > 0.5:
                filenames = list(reversed(filenames))

        for num, elm in enumerate(all_requests):
            yield elm, float(num / len(all_requests)) * 100.


class SizeFocusedDataset(GenFunction):

    """Dataset to test the different distribution of file sizes."""

    def __init__(self, num_files: int, min_file_size: int, max_file_size: int,
                 noise_min_file_size: int, noise_max_file_size: int,
                 perc_noise: float, perc_files_x_day: float,
                 size_generator_function: str):
        """Initialize the size function parameters.

        :param num_files: total number of files
        :type num_files: int
        :param min_file_size: minumum size of the files
        :type min_file_size: int
        :param max_file_size: maximum size of the files
        :type max_file_size: int
        :param noise_min_file_size: minimum size of the noise files
        :type noise_min_file_size: int
        :param noise_max_file_size: maximum size of the noise files
        :type noise_max_file_size: int
        :param perc_noise: percentage of noise files
        :type perc_noise: float
        :param perc_files_x_day: percentage of files per day (selected files)
        :type perc_files_x_day: float
        :param size_generator_function: name of the size generator function
        :type size_generator_function: str
        """
        super().__init__()
        self._num_files: int = num_files
        self._min_file_size: int = min_file_size
        self._max_file_size: int = max_file_size
        self._noise_min_file_size: int = noise_min_file_size
        self._noise_max_file_size: int = noise_max_file_size
        self._perc_noise: float = perc_noise
        self._perc_files_x_day: float = perc_files_x_day
        self._size_generator_function: str = size_generator_function

        num_noise_files = int((num_files / 100.) * self._perc_noise)
        num_normal_files = num_files - num_noise_files

        self._files = {
            **gen_random_files(
                num_normal_files, min_file_size, max_file_size,
                size_generator_function,
            ),
            **gen_random_files(
                num_noise_files, noise_min_file_size, noise_max_file_size,
                size_generator_function,
                start_from=num_normal_files
            )
        }

    def __repr__(self):
        return "Size Focused Dataset"

    def gen_day_elements(self, max_num: int = -1) -> Generator:
        """Generates all the day's entries.

        :param max_num: maximum number of requests, defaults to -1
        :type max_num: int, optional
        :yield: the percentage of work done
        :rtype: Generator[int, None, None]
        """
        all_requests = []
        file_perc_x_day = self._perc_files_x_day / 100.

        filenames = list(self._files.keys())
        num_visible_files = int(len(self._files) * file_perc_x_day)

        random.shuffle(filenames)
        filenames = filenames[:num_visible_files]

        while len(all_requests) < max_num:
            random.shuffle(filenames)
            for cur_file in filenames:
                if len(all_requests) == max_num:
                    break
                all_requests.append({
                    'Filename': cur_file,
                    **self._files[cur_file].copy(),
                })

        for num, elm in enumerate(all_requests):
            yield elm, float(num / len(all_requests)) * 100.
