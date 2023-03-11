**Dash Compose provides a tidier way of composing Plotly Dash layouts.**
Read about the motivation behind it [here](motivation.md).
I'm going to assume you already know how to build Dash applications, so let's get straight into an example!

## Hello world!

The code below is a complete Dash application, in which Dash Compose has been used to create a small tree of Dash components for the application's layout.

```py title="hello_world.py" linenums="1"
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
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

When rendered as HTML, this looks like

```html
<div>
    <span>Hello </span>
    <span>world!</span>
</div>
```

Let's step through the layout portion of the example and see what's going on.

## Compositions

```py linenums="6" hl_lines="1 2 7"
@composition
def hello_world():
    with Div() as container:
        yield Span("Hello ")
        with Span():
            yield "world!"
    return container
```

Compositions are created by decorating a function, in this case `hello_world`, with `@composition`.
There are no restrictions on the kinds of inputs this function takes, or on the outputs it returns.
The role of the `@composition` decorator is only to instantiate the parent-child relationships that your function describes.
Here, our function takes no inputs, and returns one output.

## Context managers

```py linenums="6" hl_lines="3 4"
@composition
def hello_world():
    with Div() as container:
        yield Span("Hello ")
        with Span():
            yield "world!"
    return container
```

Within your function you can use Dash components as context-managers.
This specifies that they will be the parent in one or more parent-child relationship.
To specify a child in that relationship, you can use the `yield` statement after the context has been entered.
Within a component's context, you can have multiple `yield` statements, or indeed any Python code you like.
Here, we have yielded a `Span` within a `Div`, so the `Span` becomes a child of the `Div`.

## Nested contexts

```py linenums="6" hl_lines="3 5"
@composition
def hello_world():
    with Div() as container:
        yield Span("Hello ")
        with Span():
            yield "world!"
    return container
```

Nesting context managers is another way you can specify a parent-child relationship.
In this case, the `Span` managing the inner context will become a child of the `Div` managing the outer context.

```py linenums="6" hl_lines="5 6"
@composition
def hello_world():
    with Div() as container:
        yield Span("Hello ")
        with Span():
            yield "world!"
    return container
```

When you have nested context managers, `yield` statements will create parent-child relationships based on the most recently entered context.
In this case, `"world!"` becomes a child of `Span`, and only has an indirect (grand-parent) relationship with the outer `Div`.
Note here that we have yielded something that isn't a Dash component!
This is fine: You are able to yield any Python object that is a valid child of a Dash component.
