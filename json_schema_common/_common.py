from typing import TypeAlias


__all__ = (
    'NotSetSentinel',
    'NOT_SET',
)


class NotSetSentinel:
    pass

NOT_SET = NotSetSentinel()


EncodingId: TypeAlias = str
