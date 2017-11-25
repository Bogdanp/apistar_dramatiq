import dramatiq
import functools

from .injector import inject


@functools.wraps(dramatiq.actor)
def actor(fn=None, *, app=None, **kwargs):
    def decorator(fn):
        return dramatiq.actor(inject(fn, app=app), **kwargs)

    if fn is None:
        return decorator
    return decorator(fn)
