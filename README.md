# Description

This package provides an new way of composing collections of Plotly Dash components.

In a typical Dash application, children are attached to parent components as either the first argument or via the children keyword argument.
Either approach can lead to verbose code, with lines dedicated entirely to parentheses and many layers of indentation (especially when deep trees of components are constructed).

This package supports a tidier approach.
The basic idea is that you define compositions of Dash components via generator functions.
These generators should yield Dash components, and they should be structured using Dash components as context managers.
- If a component is yielded from within the context of another component, it will become a child of that component.
- If contexts are nested, then the component managing the inner context will become a child of the component managing the outer context.
- If you attempt to yield a component without first entering another component's context, then an exception will be thrown.
Scroll down to see examples of what this looks like in practice!

The instantiation of parent-child relationships is achieved through the `@compose` decorator.
This will take your generator function and transform it into a regular function.
That function will take the same inputs and return whatever output your original generator returns.
Note that it will not return a generator object, unlike the original generator function!

# Usage

```
from dash import Dash
from dash.html import Div, Span

from dash_compose import compose


@compose
def hello_world():
    with Div() as container:
        yield Span("Hello ")
        with Span():
            yield "world"
            yield "!"
    return container


app = Dash()
app.layout = hello_world()


if __name__ == "__main__":
    app.run_server(debug=True)
```