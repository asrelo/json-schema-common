from collections.abc import Callable
import functools
import pathlib
from typing import Optional, TypeVar
import urllib.parse

from referencing.exceptions import NoSuchResource
from referencing.typing import Retrieve

from .retrieval import to_maybe_cached_resource

__all__ = (
    'retrieve_text_from_filesystem',
    'build_retrieve_from_filesystem',
)

D = TypeVar('D')

def retrieve_text_from_filesystem(
    uri, uri_base, path, *, encoding='utf-8', open_buffering: int = -1,
):
    # here scheme is a default value:
    uri_split = urllib.parse.urlsplit(uri, scheme='')
    uri_base_split = urllib.parse.urlsplit(uri_base, scheme='')
    if uri_split.scheme != uri_base_split.scheme:
        raise NoSuchResource(uri)
    if uri_base_split.query:    # absent value is empty string
        raise ValueError(f'uri_base is not allowed to have query, but it was given: {uri_base}')
    if uri_split.query:         # absent value is empty string
        raise NoSuchResource(uri)
    # XXX: abuse?
    uri_path = pathlib.PurePosixPath(uri_split.path)
    uri_base_path = pathlib.PurePosixPath(uri_base_split.path)
    try:
        path_diff = uri_path.relative_to(uri_base_path) # walk_up=False
    except ValueError as err:
        raise NoSuchResource(uri) from err
    file_path = pathlib.Path(path) / path_diff
    with open(
        file_path, 'rt', buffering=open_buffering, encoding=encoding, closefd=True, opener=None,
    ) as file:
        return file.read()

def build_retrieve_from_filesystem(
    uri_base,
    path,
    *, cache: Optional[Callable[[Retrieve[D]], Retrieve[D]]] = None,
    encoding='utf-8',
    open_buffering: int = -1,
) -> Callable[[Callable[[str], object]], Retrieve[D]]:
    retrieve_text_from_filesystem_fn = functools.partial(
        retrieve_text_from_filesystem,
        uri_base=uri_base, path=path, encoding=encoding, open_buffering=open_buffering,
    )
    return to_maybe_cached_resource(cache)(retrieve_text_from_filesystem_fn)
