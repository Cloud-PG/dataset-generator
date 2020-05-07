import importlib

from .. import functions


def get_functions():
    importlib.reload(functions)
    return [
        {'label': elm, 'value': elm}
        for elm in dir(functions)
        if callable(getattr(functions, elm))
    ]


def call_function(name: str, *args, **kwargs):
    fun = getattr(functions, name)
    return fun(*args, **kwargs)
