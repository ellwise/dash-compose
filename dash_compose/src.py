from abc import ABC, abstractmethod
from collections import defaultdict
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


def _get_generator_id():
    # _get_generator_id >> __enter__/__exit__ >> Component? >> Composition.__call__.composer
    return id(currentframe().f_back.f_back.f_back.f_locals["generator"])


def __enter__(self):
    stack_id = _get_generator_id()  # identify the generator
    stack = Component._stack[stack_id]  # and fetch its stack
    if stack:  # if there's a current context
        stack[-1] += self  # add self to it
    stack.append(self)  # replace current context with self
    return self


def __exit__(self, *args):
    stack_id = _get_generator_id()  # identify the generator
    Component._stack[stack_id].pop(-1)  # remove the last context (which will be self)


Component.__iadd__ = __iadd__
Component.__enter__ = __enter__
Component.__exit__ = __exit__
Component._stack = defaultdict(list)


Child = Union[Component, Any]
Renderer = Generator[Child, None, Any]


def compose(func: Callable[..., Renderer]) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        generator = func(*args, **kwargs)
        stack_id = id(generator)
        stack = Component._stack[stack_id]
        try:
            while True:
                component = next(generator)
                stack[-1] += component
        except StopIteration as stop:
            return stop.value

    return wrapper


class Composition(ABC):
    @abstractmethod
    def render(self, *args, **kwargs) -> Renderer:
        pass

    def __call__(self, *args, **kwargs):
        composer = compose(self.render)
        return composer(*args, **kwargs)
