# Description

This package provides an alternative way of composing collections of Plotly Dash components.

In a typical Dash application, children are attached to parent components as either the first argument or via the children keyword argument.
Either approach can lead to verbose code, with lines dedicated entirely to parentheses and many layers of indentation (especially when deep trees of components are constructed).

This package supports an alternative approach.
The basic idea is that you define generator functions that yield Dash components, and structure those functions using Dash components as context managers.
If a component is yielded from within the context of another component, it will become a child of that component.
If contexts are nested, then the component managing the inner context will become a child of the component managing the outer context.
Scroll down to see examples of what this looks like in practice.

There are two approaches you can take to instantiate the parent-child relationships you've specified.
The first is to decorate your generator function with `@compose`.
This will transform it into an ordinary function that takes the same inputs and returns the same outputs, rather than returning a generator.
The second is to define your generator function as the `render` method of a class that inherits from `Composition`.
Objects of this class can then be called like ordinary functions.
Under the hood these approaches are identical: `dash-compose` uses the `@compose` decorator within `Composition.__call__` to wrap `Composition.render`.

# Usage

```
from dash import Dash
from dash.html import Div, Span

from dash_compose import Composition, compose


@compose
def hello():
    with Span() as layout:
        yield "Hello "
    return layout


class HelloWorld(Composition):
    @staticmethod
    def render():
        with Div() as layout:
            with Div():
                yield hello()
                yield "world!"
        return layout


hello_world = HelloWorld()

app = Dash()
app.layout = hello_world()


if __name__ == "__main__":
    app.run_server(debug=True)
```