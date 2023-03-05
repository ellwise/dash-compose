from abc import ABC, abstractmethod
from collections import defaultdict
from threading import current_thread
from typing import Any, Generator, Union

from dash.development.base_component import Component


def __iadd__(self, child):
    if self.children is None:
        self.children = child
    elif isinstance(self.children, list):
        self.children.append(child)
    else:
        self.children = [self.children, child]
    return self


def __enter__(self):
    thread_id = current_thread()  # identify the thread
    stack = Component._stack[thread_id]  # and fetch its stack
    if stack:  # if there's a current context
        stack[-1] += self  # add self to it
    stack.append(self)  # replace current context with self
    return self


def __exit__(self, *args):
    thread_id = current_thread()  # identify the thread
    Component._stack[thread_id].pop(-1)  # remove the last context (which will be self)


Component.__iadd__ = __iadd__
Component.__enter__ = __enter__
Component.__exit__ = __exit__
Component._stack = defaultdict(list)


Child = Union[Component, Any]


class Composition(ABC):
    @abstractmethod
    def render(self, *args, **kwargs) -> Generator[Child, None, Any]:
        pass

    def __call__(self, *args, **kwargs):
        thread_id = current_thread()
        stack = Component._stack[thread_id]
        generator = self.render(*args, **kwargs)
        try:
            while True:
                component = next(generator)
                stack[-1] += component
        except StopIteration as stop:
            return stop.value
