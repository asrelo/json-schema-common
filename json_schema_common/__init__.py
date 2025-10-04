from collections.abc import Callable
from pathlib import Path
from typing import Optional, TypeVar

from referencing.typing import Retrieve

from ._common import *
from .registries import build_retrieve_from_filesystem

D = TypeVar('D')

_PACKAGE_PATH = Path(__file__).parent

BUNDLED_SCHEMAS_URI_BASE: str = 'file:///json_schema_common/schemas'
BUNDLED_SCHEMAS_PATH: Path = _PACKAGE_PATH / 'schemas'
_BUNDLED_SCHEMAS_ENCODING: str = 'utf-8'

def build_retrieve_bundled_schemas(
    *, cache: Optional[Callable[[Retrieve[D]], Retrieve[D]]] = None,
    open_buffering: int = -1,
) -> Callable[[Callable[[str], object]], Retrieve[D]]:
    return build_retrieve_from_filesystem(
        BUNDLED_SCHEMAS_URI_BASE, BUNDLED_SCHEMAS_PATH,
        cache=cache, encoding=_BUNDLED_SCHEMAS_ENCODING, open_buffering=open_buffering,
    )
