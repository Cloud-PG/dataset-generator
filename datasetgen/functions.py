import random

from numpy import random as np_random

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
        self._day_idx = value
        return self

    @property
    def num_req_x_day(self):
        return self.num_req_x_day

    @num_req_x_day.setter
    def num_req_x_day(self, value: int):
        self._num_req_x_day = value
        return self

    def gen_day_elements(self, max_num: int = -1):
        raise NotImplementedError

    @property
    def name(self):
        return repr(self)


class RandomGenerator(GenFunction):

    def __init__(self, num_files: int, min_file_size: int, max_file_size: int,
                 size_generator_function: str):
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

    def gen_day_elements(self, max_num: int = -1):
        filenames: list = list(self._files.keys())
        for _ in range(max_num):
            cur_file = random.choice(filenames)
            yield {
                'Filename': cur_file,
                'Size': self._files[cur_file]['Size'],
                'Protocol': self._files[cur_file]['Protocol'],
            }, None


class HighFrequencyDataset(GenFunction):

    def __init__(self, num_files: int, min_file_size: int, max_file_size: int,
                 lambda_less_req_files: float, lambda_more_req_files: float,
                 perc_more_req_files: float, perc_files_x_day: float,
                 size_generator_function: str):
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

    def __repr__(self):
        return "High Frequency Dataset"

    def gen_day_elements(self, max_num: int = -1):
        more_req_files_freq = np_random.poisson(
            lam=self._lambda_more_req_files, size=self._num_more_req_files
        )
        less_req_files_freq = np_random.poisson(
            lam=self._lambda_less_req_files, size=self._num_less_req_files
        )

        all_requests = []

        for idx, (cur_file, file_info) in enumerate(self._more_req_files.items()):
            if random.random() * 100. <= self._perc_files_x_day:
                for _ in range(more_req_files_freq[idx]):
                    all_requests.append({
                        'Filename': cur_file,
                        **file_info,
                    })

        for idx, (cur_file, file_info) in enumerate(self._less_req_files.items()):
            if random.random() * 100. <= self._perc_files_x_day:
                for _ in range(less_req_files_freq[idx]):
                    all_requests.append({
                        'Filename': cur_file,
                        **file_info,
                    })

        random.shuffle(all_requests)

        for num, elm in enumerate(all_requests):
            yield elm, float(num / len(all_requests)) * 100.


class RecencyFocusedDataset(GenFunction):

    def __init__(self, num_files: int, min_file_size: int, max_file_size: int,
                 perc_noise: float, perc_files_x_day: float,
                 size_generator_function: str):
        super().__init__()
        self._num_files: int = num_files
        self._min_file_size: int = min_file_size
        self._max_file_size: int = max_file_size
        self._perc_noise: float = perc_noise
        self._perc_files_x_day: float = perc_files_x_day
        self._size_generator_function: str = size_generator_function

        self._files = gen_random_files(
            num_files, min_file_size, max_file_size,
            size_generator_function
        )

    def __repr__(self):
        return "Recency Focused Dataset"

    def gen_day_elements(self, max_num: int = -1):
        all_requests = []
        file_perc_x_day = self._perc_files_x_day / 100.
        perc_noise = self._perc_noise / 100.
        all_file_names = list(self._files.keys())
        max_num_req = random.randint(2, max_num)

        while len(all_requests) < max_num:
            for cur_file, file_info in self._files.items():
                if random.random() <= file_perc_x_day:
                    if len(all_requests) == max_num:
                        break
                    num_requests = random.randint(1, max_num_req)
                    for _ in range(num_requests):
                        if random.random() <= perc_noise:
                            noise_file = random.choice(all_file_names)
                            noise_file_info = self._files[noise_file]
                            all_requests.append({
                                'Filename': noise_file,
                                **noise_file_info,
                            })
                        else:
                            all_requests.append({
                                'Filename': cur_file,
                                **file_info,
                            })
                        if len(all_requests) == max_num:
                            break

        for num, elm in enumerate(all_requests):
            yield elm, float(num / len(all_requests)) * 100.
