from collections.abc import Callable
import json
from typing import Any, TypeAlias, TypeVar

from referencing import Resource
from referencing.exceptions import NoSuchResource
from referencing.typing import Retrieve

__all__ = (
    'RetrieveTextFn',
    'RetrieveFunctionsChain',
    'schema_text_to_data',
    'LOADS_FN_DEFAULT',
)

D = TypeVar('D')

RetrieveTextFn: TypeAlias = Callable[[str], str]

# goofy but works?
class RetrieveFunctionsChain(list[Retrieve[D]], Retrieve[D]):
    def __call__(self, uri: str) -> Resource[D]:
        for retrieve in self:
            try:
                return retrieve(uri)
            except NoSuchResource:
                pass
        raise NoSuchResource(uri)

def schema_text_to_data(text: str) -> Any:
    # XXX: pass a 'cls' kwarg?
    return json.loads(text)

LOADS_FN_DEFAULT: Callable[[str], Any] = schema_text_to_data
