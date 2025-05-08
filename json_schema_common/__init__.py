import pathlib

from json_schema_common.registries import build_filesystem_registry

_PACKAGE_PATH = pathlib.Path(__file__).parent

BUNDLED_SCHEMAS_URI_BASE = 'file:///json_schema_common/schemas'
BUNDLED_SCHEMAS_PATH = _PACKAGE_PATH / 'schemas'

def build_bundled_schemas_registry(*, open_buffering=-1):
    return build_filesystem_registry(
        BUNDLED_SCHEMAS_URI_BASE, BUNDLED_SCHEMAS_PATH, open_buffering=open_buffering,
    )
