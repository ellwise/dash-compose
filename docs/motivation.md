# Motivation

## Readability of component trees

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

## Locality of layout and logic

There's been a trend in web-development away from "separation of concerns" and towards greater "locality".
Where classic web-development separates layout (HTML) from logic (Javascript) and from style (CSS), React has broken down the layout/logic wall, and more recently tailwindcss has broken down the layout/style wall.
The result is that codebases have become more comprehensible to developers as related pieces of code are now closer together.

To illustrate how Dash Compose can increase the locality of your code, consider the the tabs below.
They have been adapted from the Plotly Dash documentation [here](https://dash.plotly.com/basic-callbacks).

- **Dash**: There is a clear separation in code between the application's layout (lines 12-24) and logic (lines 27-52). This approach is natural in regular Dash because the specification of a tree of components is done via the constructors for those components, and there's only so much a developer can do by writing inline Python within those constructor statements.
- **Dash Compose**: Layout and logic now intermingle because context managers and `yield` statements can be placed freely within a composition function. We've chosen to place the logic associated with updating an output component alongside that component's definition, since each output can only have one associated callback function. We've then been able to add comments to the code in a "narrative" structure, rather than referring forwards/backwards to other parts of the file.

=== "Dash"

    ```py linenums="1"
    # -*- coding: utf-8 -*-
    from dash import Dash, Input, Output, dcc, html

    external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

    app = Dash(__name__, external_stylesheets=external_stylesheets)

    all_options = {
        "America": ["New York City", "San Francisco", "Cincinnati"],
        "Canada": ["Montréal", "Toronto", "Ottawa"],
    }
    app.layout = html.Div(
        [
            dcc.RadioItems(
                list(all_options.keys()),
                "America",
                id="countries-radio",
            ),
            html.Hr(),
            dcc.RadioItems(id="cities-radio"),
            html.Hr(),
            html.Div(id="display-selected-values"),
        ]
    )


    @app.callback(
        Output("cities-radio", "options"),
        Input("countries-radio", "value"),
    )
    def set_cities_options(selected_country):
        return [{"label": i, "value": i} for i in all_options[selected_country]]


    @app.callback(
        Output("cities-radio", "value"),
        Input("cities-radio", "options"),
    )
    def set_cities_value(available_options):
        return available_options[0]["value"]


    @app.callback(
        Output("display-selected-values", "children"),
        Input("countries-radio", "value"),
        Input("cities-radio", "value"),
    )
    def set_display_children(selected_country, selected_city):
        return "{} is a city in {}".format(
            selected_city,
            selected_country,
        )


    if __name__ == "__main__":
        app.run_server(debug=True)
    ```

=== "Dash Compose"

    ```py linenums="1"
    # -*- coding: utf-8 -*-
    from dash import Dash, Input, Output, dcc, html
    from dash_compose import composition

    external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

    all_options = {
        "America": ["New York City", "San Francisco", "Cincinnati"],
        "Canada": ["Montréal", "Toronto", "Ottawa"],
    }


    @composition
    def render(app):
        with html.Div() as layout:
            # render a set of radio-items for the countries
            yield dcc.RadioItems(
                list(all_options.keys()),
                "America",
                id="countries-radio",
            )

            # render a set of radio-items for the cities
            yield html.Hr()
            yield dcc.RadioItems(id="cities-radio")

            # the city options depend on the selected country
            @app.callback(
                Output("cities-radio", "options"),
                Input("countries-radio", "value"),
            )
            def set_cities_options(selected_country):
                return [
                    {"label": i, "value": i}
                    for i in all_options[selected_country]
                ]

            # if the city options change (because we changed country)
            # then automatically select the first
            @app.callback(
                Output("cities-radio", "value"),
                Input("cities-radio", "options"),
            )
            def set_cities_value(available_options):
                return available_options[0]["value"]

            # render some text explaining the selected options
            yield html.Hr()
            yield html.Div(id="display-selected-values")

            @app.callback(
                Output("display-selected-values", "children"),
                Input("countries-radio", "value"),
                Input("cities-radio", "value"),
            )
            def set_display_children(selected_country, selected_city):
                return "{} is a city in {}".format(
                    selected_city,
                    selected_country,
                )

        return layout


    app = Dash(__name__, external_stylesheets=external_stylesheets)
    app.layout = render(app)


    if __name__ == "__main__":
        app.run_server(debug=True)
    ```