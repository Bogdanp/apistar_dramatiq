import apistar
import functools
import inspect
import typing

from apistar.components import dependency
from apistar.exceptions import CouldNotResolveDependency
from apistar.interfaces import Resolver
from apistar.types import KeywordArgs, ParamName
from threading import Lock

#: Instantiating and running an injector for the first time takes on
#: the order of 30ms so we need to cache it globally.
_injector = None
_injector_mutex = Lock()


#: A mapping from positional argument names to their positions in the
#: signature.
ArgPositions = typing.Dict[str, int]

#: A list of positional argument names.
PositionalArgs = typing.Iterable[str]


class FnResolver(Resolver):
    def resolve(self, param, func):
        return (f"fnarg:{param.name}", self.get_arg)

    def get_arg(self,
                name: ParamName,
                poss: ArgPositions,
                args: PositionalArgs,
                kwargs: KeywordArgs) -> typing.Any:
        try:
            return kwargs[name]
        except KeyError:
            try:
                return args[poss[name]]
            except (KeyError, IndexError):
                msg = "Injector could not resolve parameter %r" % name
                raise CouldNotResolveDependency(msg)


def get_injector(app=None):
    global _injector

    if not _injector:
        with _injector_mutex:
            if not _injector:
                app = app or apistar.get_current_app()
                _injector = dependency.DependencyInjector(
                    components=app.components,
                    initial_state=app.preloaded_state,
                    required_state={
                        ArgPositions: "poss",
                        PositionalArgs: "args",
                        KeywordArgs: "kwargs",
                    },
                    resolvers=[FnResolver()],
                )

    return _injector


def inject(fn=None, *, app=None):
    """Makes any callable dependency-injectable.

    Parameters:
      fn(callable): The callable to decorate.
      app(apistar.App): The application to use for DI.  If this is not
        provided, the app will be looked up dynamically.

    Returns:
      callable
    """
    def decorator(fn):
        # Precompute posargs positions in the signature.
        poss = {param: i for i, param in enumerate(inspect.signature(fn).parameters)}

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            return get_injector(app).run(fn, {
                "poss": poss,
                "args": args,
                "kwargs": kwargs,
            })

        return wrapper

    if fn is None:
        return decorator
    return decorator(fn)
