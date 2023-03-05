# Description

This package provides an alternative way of composing collections of Plotly Dash components.

In a typical Dash application, children are attached to parent components as either the first argument or via the children keyword argument.
Either approach can lead to verbose code, with lines dedicated entirely to parentheses and many layers of indentation (especially when deep trees of components are constructed).

This package supports an alternative approach:
- An abstract `Composition` class is provided for creating compositions of Dash components.
- That class requires a `render` method to be defined - this should yield Dash components.
- Within the `render` method, components can be used as context managers.
- If a component is yielded from within another component's context, it will become a child of that component.
- If a component is used as a context manager from within another component's context, it will also become a child of that component.
- Those parent-child relationships are instantiated when the `Composition` object is called.

# Usage

```
from dash import Dash
from dash.html import Div, Span

from dash_compose import Composition


class Layout(Composition):
    @staticmethod
    def render():
        with Div() as layout:
            with Div():
                yield Span("Hello")
                yield " "
                yield Span("world!")
        return layout


app = Dash()
app.layout = Layout()

if __name__ == "__main__":
    app.run_server(debug=True)
```