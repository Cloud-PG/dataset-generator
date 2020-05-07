import random
from itertools import combinations_with_replacement
from string import ascii_letters


def base_function(num_files: int, min_file_size: int, max_file_size: int):
    file_len = 1
    files = ascii_letters[:]
    while len(files) < num_files:
        files = ["".join(tuple_)
                 for tuple_ in combinations_with_replacement(files, file_len)]
        file_len += 1
    files = files[:num_files]

    while True:
        yield {
            'Filename': random.choice(files),
            'Size': float(random.randint(min_file_size, max_file_size))
        }
