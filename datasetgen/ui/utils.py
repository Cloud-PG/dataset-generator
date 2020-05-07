import importlib

from .. import functions
from inspect import getmodule


def get_functions():
    importlib.reload(functions)
    return [
        {'label': elm, 'value': elm}
        for elm in dir(functions)
        if callable(getattr(functions, elm)) and \
            getmodule(getattr(functions, elm)).__name__ == 'datasetgen.functions'
    ]
