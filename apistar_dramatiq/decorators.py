import dramatiq
import functools

from .injector import inject


@functools.wraps(dramatiq.actor)
def actor(fn=None, **kwargs):
    def decorator(fn):
        return dramatiq.actor(inject(fn), **kwargs)

    if fn is None:
        return decorator
    return decorator(fn)
