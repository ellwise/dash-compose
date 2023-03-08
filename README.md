# Description

**Dash Compose provides a tidier way of composing Plotly Dash layouts.**

In a typical Dash application, children are attached to parent components as either the first argument or via the children keyword argument.
Either approach can lead to verbose code, with lines dedicated entirely to parentheses and many levels of indentation (especially when deep trees of components are constructed, and when code formatting tools like `black` are used).

`dash-compose` alleviates this issue by allowing compositions of Dash components to be defined via specially structured generator functions.
These generators should yield Dash components, and they should be structured using Dash components as context managers.
- If a component is yielded from within the context of another component, it will become a child of that component.
- If contexts are nested, then the component managing the inner context will become a child of the component managing the outer context.
- If you attempt to yield a component without first entering another component's context, then an exception will be thrown.
Scroll down to see examples of what this looks like in practice!

The instantiation of parent-child relationships is achieved through the `@composition` decorator.
This will take your generator function and transform it into a regular function.
That function will take the same inputs and return whatever output your original generator returns.
Note that it will not return a generator object, unlike the original generator function!

# Usage

## Hello world!

Below is a very simple example showing how to use `dash-compose` to nest component contexts and yield child components within them.

```
from dash import Dash
from dash.html import Div, Span

from dash_compose import composition


@composition
def hello_world():
    with Div() as container:
        yield Span("Hello ")
        with Span():
            yield "world!"
    return container


app = Dash()
app.layout = hello_world()


if __name__ == "__main__":
    app.run_server(debug=True)
```

This layout is equivalent to the HTML below.

```
<div>
    <span>Hello </span>
    <span>world!</span>
</div>
```

## A more complex example

A second example has been adapted from the Plotly Dash documentation [here](https://dash.plotly.com/layout).
It includes a more complex layout than the example above.

```
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from dash_compose import composition


@composition
def layout():
    with html.Div() as container:
        yield dcc.Input(id="num-multi", type="number", value=5)
        with html.Table():
            with html.Tr():
                yield html.Td(["x", html.Sup(2)])
                yield html.Td(id="square")
            with html.Tr():
                yield html.Td(["x", html.Sup(3)])
                yield html.Td(id="cube")
            with html.Tr():
                yield html.Td([2, html.Sup("x")])
                yield html.Td(id="twos")
            with html.Tr():
                yield html.Td([3, html.Sup("x")])
                yield html.Td(id="threes")
            with html.Tr():
                yield html.Td(["x", html.Sup("x")])
                yield html.Td(id="x^x")
    return container


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = layout()


@app.callback(
    Output("square", "children"),
    Output("cube", "children"),
    Output("twos", "children"),
    Output("threes", "children"),
    Output("x^x", "children"),
    Input("num-multi", "value"),
)
def callback_a(x):
    return x**2, x**3, 2**x, 3**x, x**x


if __name__ == "__main__":
    app.run_server(debug=True)
```

To give a sense of the tidiness and brevity `dash-compose` provides, you can compare the `layout` function above to an equivalently structured function below.
The latter has been formatted using `black`.
It is twice as long (with half those lines for parentheses or braces), and it contains three extra levels of indentation.

```
def layout():
    return html.Div(
        [
            dcc.Input(id="num-multi", type="number", value=5),
            html.Table(
                [
                    html.Tr(
                        [
                            html.Td(["x", html.Sup(2)]),
                            html.Td(id="square"),
                        ]
                    ),
                    html.Tr(
                        [
                            html.Td(["x", html.Sup(3)]),
                            html.Td(id="cube"),
                        ]
                    ),
                    html.Tr(
                        [
                            html.Td([2, html.Sup("x")]),
                            html.Td(id="twos"),
                        ]
                    ),
                    html.Tr(
                        [
                            html.Td([3, html.Sup("x")]),
                            html.Td(id="threes"),
                        ]
                    ),
                    html.Tr(
                        [
                            html.Td(["x", html.Sup("x")]),
                            html.Td(id="x^x"),
                        ]
                    ),
                ]
            ),
        ]
    )
```