from functools import wraps
from inspect import currentframe
from typing import Any, Callable, Generator, Union

from dash.development.base_component import Component


def __iadd__(self, child):
    """Add a child to this component's children"""
    if self.children is None:
        self.children = child
    elif isinstance(self.children, list):
        self.children.append(child)
    else:
        self.children = [self.children, child]
    return self


def _get_contexts():
    """Fetch contexts from the @compose decorator via the call stack"""
    # _get_contexts >> __enter__/__exit__ >> func >> wrapper
    return currentframe().f_back.f_back.f_back.f_locals["contexts"]


def __enter__(self):
    """Add self as a child to any existing context, then add self to the list of contexts"""
    contexts = _get_contexts()  # fetch the context stack from a calling frame
    if contexts:  # if there's an active context
        contexts[-1] += self  # add self to its children
    contexts.append(self)  # replace the active context with self
    return self


def __exit__(self, *args):
    """Remove self from the list of contexts"""
    contexts = _get_contexts()  # fetch the context stack from a calling frame
    contexts.pop(-1)  # remove the currently active context (this will be self)


# patch the Component class to enable easy addition of children
Component.__iadd__ = __iadd__

# patch the Component class to allow use as a context manager
Component.__enter__ = __enter__
Component.__exit__ = __exit__


# define some type aliases for communicating the intent of compose
Child = Union[Component, Any]  # any valid Dash component
Composer = Generator[Child, None, Any]  # a dash-compose generator


def composition(func: Callable[..., Composer]) -> Callable[..., Any]:
    """Instantiate parent-child relationships specified by a dash-compose generator function"""

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        contexts = []  # a stack containing all active context managers
        # contexts will be fetched through the call stack by context managers within the generator
        composer = func(*args, **kwargs)  # instantiate the Composer
        try:  # fetch components from the Composer until it is exhausted
            while True:
                component = next(composer)  # proceed to the next component that is yielded
                if not contexts:  # throw an exception if there is no active context
                    raise Exception(f"Cannot yield {component} outside a context manager.")
                contexts[-1] += component  # add to the current context's children
        except StopIteration as stop:
            return stop.value  # return the same value as the original composer

    return wrapper
