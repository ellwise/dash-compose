# Description

This package provides an alternative way of composing collections of Plotly Dash components.

In a typical Dash application, children are attached to parent components as either the first argument or via the children keyword argument.
Either approach can lead to verbose code, with lines dedicated entirely to parentheses and many layers of indentation (especially when deep trees of components are constructed).

This package supports an alternative approach:
- Compositions of Dash components are defined using generator functions along with a `compose` decorator.
- Within those generator functions, Dash components can be used as context managers.
- If a component is yielded from within another component's context, it will become a child of that component.
- If a component is used as a context manager from within another component's context, it will also become a child of that component.

# Usage

```
from dash import Dash
from dash.html import Div, Span

from dash_compose import compose


@compose
def render():
    with Div() as layout:
        with Div():
            yield Span("Hello")
            yield " "
            yield Span("world!")
    return layout


app = Dash()
app.layout = render()

if __name__ == "__main__":
    app.run_server(debug=True)
```