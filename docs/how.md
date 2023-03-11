# How does it work?

## Patching Plotly Dash

Dash Compose patches the `dash.development.base_component.Component` to provide three extra methods.
This patching occurs as soon as Dash Compose is imported, and affects all Dash components (including third-party ones) since they are derived from this class.

1. The `__iadd__` method has been added to make it easier to add children to an existing Dash component. This method neatly handles the cases where the parent component has its `children` property set to `None`, a single value, or a list of values.
2. The `__enter__` and `__exit__` methods have been added so that Dash components can be used as context managers. The `__enter__` method returns the component itself for convenience. Both methods are heavily coupled to the `composition` decorator.

## Tracking contexts

Within the `composition` function, a stack of components is maintained.
Whenever a context is entered, the Dash component managing it is added to the stack.
When it is exited, the component is removed from the stack.
Maintenance of this context stack is a bit magical: The `__enter__` and `__exit__` methods use `inspect` to traverse Python's call stack upwards into the `composition` function so they can append and remove elements from it.

## Interpreting compositions

Compositions are defined via user-supplied generator functions.
However, these functions no longer return `generator` objects after the `@composition` decorator has been applied!
Instead, they are transformed into ordinary functions that take the same inputs, and return the same outputs.

During this transformation, `composition` instantiates and exhausts the generator.
In doing so, any `yielded` values are added as children to whichever Dash component is currently sitting at the top of the context stack, and the context stack is updated as contexts are entered and exited.
The `StopIteration` exception is caught during this execution so that `composition` can return whatever value was returned by the user in their composition's generator function.
