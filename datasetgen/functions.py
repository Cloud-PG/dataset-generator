import random
from itertools import combinations_with_replacement
from string import ascii_letters


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


class RandomGenerator(GenFunction):

    def __init__(self, num_files: int, min_file_size: int, max_file_size: int):
        super().__init__()
        self._num_files = num_files
        self._min_file_size = min_file_size
        self._max_file_size = max_file_size

        file_len = 1
        files = ascii_letters[:]
        while len(files) < num_files:
            files = ["".join(tuple_)
                     for tuple_ in combinations_with_replacement(files, file_len)]
            file_len += 1
        self._files = files[:num_files]

    def __repr__(self):
        return "Random Generator"

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self) -> 'generator':
        while True:
            yield {
                'Filename': random.choice(self._files),
                'Size': float(random.randint(self._min_file_size, self._max_file_size))
            }, False
