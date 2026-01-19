from collections.abc import Callable
from typing import Optional, TypeVar

from referencing import Resource
from referencing.retrieval import to_cached_resource as original_to_cached_resource
from referencing.typing import Retrieve

from json_schema_common._common import NotSetSentinel, NOT_SET
from ._common import RetrieveTextFn, LOADS_FN_DEFAULT

__all__ = (
    'to_resource',
    'to_cached_resource',
    'to_maybe_cached_resource',
)

D = TypeVar('D')

# TODO: type CacheFn[D] = Callable[[Retrieve[D]], Retrieve[D]]

def to_resource(
    loads: Callable[[str], D] = LOADS_FN_DEFAULT,
    from_contents: Callable[[D], Resource[D]] = Resource.from_contents,
) -> Callable[[RetrieveTextFn], Retrieve[D]]:
    def decorator(retrieve: RetrieveTextFn) -> Retrieve[D]:
        def wrapped_retrieve(uri: str) -> Resource[D]:
            response = retrieve(uri)
            contents = loads(response)
            return from_contents(contents)
        return wrapped_retrieve
    return decorator

def to_cached_resource(
    cache: Optional[Callable[[Retrieve[D]], Retrieve[D]]] = None,
    loads: Callable[[str], D] = LOADS_FN_DEFAULT,
    from_contents: Callable[[D], Resource[D]] | NotSetSentinel = NOT_SET,
) -> Callable[[RetrieveTextFn], Retrieve[D]]:
    kwargs_extra = {}
    if not isinstance(from_contents, NotSetSentinel):
        kwargs_extra['from_contents'] = from_contents
    return original_to_cached_resource(cache=cache, loads=loads, **kwargs_extra)

def to_maybe_cached_resource(
    cache: Optional[Callable[[Retrieve[D]], Retrieve[D]] | bool] = None,
    loads: Callable[[str], D] = LOADS_FN_DEFAULT,
    from_contents: Callable[[D], Resource[D]] | NotSetSentinel = NOT_SET,
) -> Callable[[RetrieveTextFn], Retrieve[D]]:
    kwargs_extra = {}
    if not isinstance(from_contents, NotSetSentinel):
        kwargs_extra['from_contents'] = from_contents
    if not cache:
        return to_resource(loads=loads, **kwargs_extra)
    return to_cached_resource(
        cache=(cache if callable(cache) else None), loads=loads, **kwargs_extra,
    )
