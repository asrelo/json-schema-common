import json

__all__ = ('schema_text_to_data',)

def schema_text_to_data(text):
    # XXX: pass a 'cls' kwarg?
    return json.loads(text)
