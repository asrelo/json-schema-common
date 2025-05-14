import json

from referencing.exceptions import NoSuchResource

__all__ = (
    'RetrieveFunctionsChain',
    'schema_text_to_data',
)

# goofy but works?
class RetrieveFunctionsChain(list):
    def __call__(self, uri):
        for retrieve in self:
            try:
                return retrieve(uri)
            except NoSuchResource:
                pass
        raise NoSuchResource(uri)

def schema_text_to_data(text):
    # XXX: pass a 'cls' kwarg?
    return json.loads(text)
