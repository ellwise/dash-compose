# Motivation

In a typical Dash application, child components are attached to parents as either the first argument to the parent's constructor, or via the `children` keyword argument.
Either approach can lead to verbose code, with lines dedicated entirely to parentheses and many levels of indentation (especially when deep trees of components are constructed, and when code formatting tools are used).
To illustrate this, consider the the tabs below.
The code within them has been adapted from the Plotly Dash documentation [here](https://dash.plotly.com/basic-callbacks).

- **Dash (Original)**: This (almost) shows the original code. Its density makes it readable, but its formatting hides the tree-structure of the components, and it doesn't match the default formatting rules of `black`.
- **Dash (Refactored)**: This shows the code after it has been refactored into a function with a clear tree-like component structure, and formatted using `black`. The length of the code has increased dramatically, almost half the lines of code are just parentheses or braces, and there are seven levels of indentation.
- **Dash Compose**: This shows the same code refactored using Dash Compose. It reduces both the number of lines of code and the number of levels of indentation, thus minimising visual noise while retaining communication of the tree-structure of the components.

=== "Dash (Original)"

    ```py linenums="1"
    layout = html.Div([
        dcc.Input(
            id='num-multi',
            type='number',
            value=5
        ),
        html.Table([
            html.Tr([html.Td(['x', html.Sup(2)]), html.Td(id='square')]),
            html.Tr([html.Td(['x', html.Sup(3)]), html.Td(id='cube')]),
            html.Tr([html.Td([2, html.Sup('x')]), html.Td(id='twos')]),
            html.Tr([html.Td([3, html.Sup('x')]), html.Td(id='threes')]),
            html.Tr([html.Td(['x', html.Sup('x')]), html.Td(id='x^x')]),
        ]),
    ])
    ```

=== "Dash (Refactored)"

    ```py linenums="1"
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

=== "Dash Compose"

    ```py linenums="1"
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
    ```
