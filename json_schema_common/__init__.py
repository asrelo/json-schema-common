import pathlib

from ._common import *
from .registries import build_retrieve_from_filesystem

_PACKAGE_PATH = pathlib.Path(__file__).parent

BUNDLED_SCHEMAS_URI_BASE = 'file:///json_schema_common/schemas'
BUNDLED_SCHEMAS_PATH = _PACKAGE_PATH / 'schemas'
_BUNDLED_SCHEMAS_ENCODING = 'utf-8'

def build_retrieve_bundled_schemas(*, cache=None, open_buffering=-1):
    return build_retrieve_from_filesystem(
        BUNDLED_SCHEMAS_URI_BASE, BUNDLED_SCHEMAS_PATH,
        cache=cache, encoding=_BUNDLED_SCHEMAS_ENCODING, open_buffering=open_buffering,
    )
