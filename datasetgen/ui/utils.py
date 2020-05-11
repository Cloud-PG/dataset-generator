import importlib

from .. import functions
from inspect import isclass


def get_functions():
    importlib.reload(functions)
    return list(sorted([
        {'label': elm, 'value': elm}
        for elm in dir(functions)
        if isclass(getattr(functions, elm)) and
        issubclass(getattr(functions, elm), functions.GenFunction) and
        getattr(functions, elm) is not functions.GenFunction
    ], key=lambda elm: elm['label']))
