import random


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

    def next(self):
        raise NotImplementedError

    @property
    def name(self):
        return repr(self)


def gen_random_files(num_files: int, min_file_size: int, max_file_size: int):
    return {
        (
            filename,
            float(random.randint(min_file_size, max_file_size))
        )
        for filename in range(num_files)
    }


class RandomGenerator(GenFunction):

    def __init__(self, num_files: int, min_file_size: int, max_file_size: int):
        super().__init__()
        self._num_files: int = num_files
        self._min_file_size: int = min_file_size
        self._max_file_size: int = max_file_size

        self._files = gen_random_files(num_files, min_file_size, max_file_size)

    def __repr__(self):
        return "Random Generator"

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self) -> 'Generator[Tuple(dict, bool)]':
        filenames: list = self._files.values()
        while True:
            cur_file = filenames
            cur_size = self._files[cur_file]
            yield {
                'Filename': cur_file,
                'Size': cur_size,
            }, False


class PoissonGenerator(GenFunction):

    def __init__(self, num_files: int, min_file_size: int, max_file_size: int,
                 lambda_less_req_files: float, lambda_more_req_files: float,
                 perc_more_req_files: float, ):
        super().__init__()
        self._num_files: int = num_files
        self._min_file_size: int = min_file_size
        self._max_file_size: int = max_file_size
        self._lambda_less_req_files: float = lambda_less_req_files
        self._lambda_more_req_files: float = lambda_more_req_files
        self._perc_more_req_files: float = perc_more_req_files

        self._files = gen_random_files(num_files, min_file_size, max_file_size)

    def __repr__(self):
        return "Poisson Generator"

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self) -> 'Generator[Tuple(dict, bool)]':
        filenames: list = self._files.values()
        while True:
            cur_file = filenames
            cur_size = self._files[cur_file]
            yield {
                'Filename': cur_file,
                'Size': cur_size,
            }, False
