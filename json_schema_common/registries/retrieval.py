from collections.abc import Callable
from typing import Optional, TypeVar

from referencing import Resource
from referencing.retrieval import to_cached_resource as original_to_cached_resource
from referencing.typing import Retrieve

from json_schema_common._common import NotSetSentinel, NOT_SET
from ._common import schema_text_to_data

__all__ = (
    'to_resource',
    'to_cached_resource',
    'to_maybe_cached_resource',
)

D = TypeVar('D')

def to_resource(loads=None, from_contents=None):
    if loads is None:
        loads = schema_text_to_data
    if from_contents is None:
        from_contents = Resource.from_contents
    def decorator(retrieve):
        def wrapped_retrieve(uri):
            response = retrieve(uri)
            contents = loads(response)
            return from_contents(contents)
        return wrapped_retrieve
    return decorator

def to_cached_resource(
    cache: Optional[Callable[[Retrieve[D]], Retrieve[D]]] = None,
    loads=None,
    from_contents=NOT_SET,
) -> Callable[[Callable[[str], object]], Retrieve[D]]:
    if loads is None:
        loads = schema_text_to_data
    kwargs_extra = {}
    if not isinstance(from_contents, NotSetSentinel):
        kwargs_extra['from_contents'] = from_contents
    return original_to_cached_resource(cache=cache, loads=loads, **kwargs_extra)

def to_maybe_cached_resource(
    cache: Optional[Callable[[Retrieve[D]], Retrieve[D]]] = None,
    loads=None,
    from_contents=NOT_SET,
) -> Callable[[Callable[[str], object]], Retrieve[D]]:
    if not cache:
        return to_resource(
            loads=loads,
            from_contents=(
                from_contents
                if (not isinstance(from_contents, NotSetSentinel))
                else None
            ),
        )
    return to_cached_resource(
        cache=(cache if callable(cache) else None), loads=loads, from_contents=from_contents,
    )
