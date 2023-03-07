from functools import wraps
from inspect import currentframe
from typing import Any, Callable, Generator, Union

from dash.development.base_component import Component


def __iadd__(self, child):
    if self.children is None:
        self.children = child
    elif isinstance(self.children, list):
        self.children.append(child)
    else:
        self.children = [self.children, child]
    return self


def _get_stack():
    # _get_stack >> __enter__/__exit__ >> func >> wrapper
    stack = currentframe().f_back.f_back.f_back.f_locals["stack"]
    return stack


def __enter__(self):
    stack = _get_stack()  # fetch the stack from a calling frame
    if stack:  # if there's a current context
        stack[-1] += self  # add self to it
    stack.append(self)  # replace current context with self
    return self


def __exit__(self, *args):
    stack = _get_stack()  # fetch the stack from a calling frame
    stack.pop(-1)  # remove the last context (which will be self)


Component.__iadd__ = __iadd__
Component.__enter__ = __enter__
Component.__exit__ = __exit__


Child = Union[Component, Any]
Composer = Generator[Child, None, Any]


def compose(func: Callable[..., Composer]) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        generator = func(*args, **kwargs)
        stack = []  # this will be fetched via calling frames by context managers in the generator
        try:
            while True:
                component = next(generator)
                if not stack:
                    raise Exception(f"Cannot yield {component} outside a context manager.")
                stack[-1] += component
        except StopIteration as stop:
            return stop.value

    return wrapper
