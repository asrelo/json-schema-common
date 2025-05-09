import functools
import pathlib
import urllib.parse

from referencing import Registry
from referencing.exceptions import NoSuchResource

from .retrieval import to_maybe_cached_resource

__all__ = (
    'retrieve_text_from_filesystem',
    'build_filesystem_registry',
)

def retrieve_text_from_filesystem(uri, uri_base, path, *, open_buffering=-1):
    # here scheme is a default value:
    uri_split = urllib.parse.urlsplit(uri, scheme='')
    uri_base_split = urllib.parse.urlsplit(uri_base, scheme='')
    if uri_split.scheme != uri_base_split.scheme:
        return NoSuchResource(uri)
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
        file_path, 'rt', buffering=open_buffering, encoding='utf-8', closefd=True, opener=None,
    ) as file:
        return file.read()

# I tried subclassing Registry, but referencing._attrs.UnsupportedSubclassing .
# There is no interface for Registry, so no good composition.
def build_filesystem_registry(uri_base, path, *, cache=None, open_buffering=-1):
    retrieve_text_from_filesystem_fn = functools.partial(
        retrieve_text_from_filesystem,
        uri_base=uri_base, path=path, open_buffering=open_buffering,
    )
    return Registry(retrieve=to_maybe_cached_resource(cache)(retrieve_text_from_filesystem_fn))
