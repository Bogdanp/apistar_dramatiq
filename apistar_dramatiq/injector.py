import functools
import inspect

from apistar import Component
from apistar.server.injector import Injector
from inspect import Parameter
from typing import Any, Callable, Dict, Iterable, List, Optional

#: The type of component lists.
Components = List[Component]

#: The global list of components.
_components: Components = []


def setup(components: Components) -> None:
    """Set up the list of components that may be dependency injected.
    """
    global _components
    _components = components


def inject(fn: Optional[Callable[..., Any]] = None, *, components: Optional[Components] = None) -> Callable[..., Any]:
    """Makes any callable dependency-injectable.

    Parameters:
      fn: The callable to decorate.
      components: The components that may be injected.

    Returns:
      Either a decorator or a decorated function whose parameters can
      be dependency-injected.
    """
    def decorator(fn):
        parameters = {name: i for i, name in enumerate(inspect.signature(fn).parameters)}

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            resolver = _ArgumentResolver(parameters, args, kwargs)
            injector = Injector([resolver, *(components or _components)], {})
            return injector.run([fn], {})

        return wrapper

    if fn is None:  # pragma: no cover
        return decorator
    return decorator(fn)


class _ArgumentResolver(Component):
    def __init__(self, parameters: Dict[str, int], args: Iterable[Any], kwargs: Dict[str, Any]) -> None:
        self.state = state = kwargs
        for name, idx in parameters.items():
            if name not in state:
                try:
                    state[name] = args[idx]
                except IndexError:
                    continue

    def can_handle_parameter(self, parameter: Parameter) -> bool:
        return parameter.name in self.state or parameter.default is not Parameter.empty

    # Return annotation can be Any because we're overwriting can_handle_parameter.
    def resolve(self, parameter: Parameter) -> Any:
        try:
            return self.state[parameter.name]
        except KeyError:
            return parameter.default
