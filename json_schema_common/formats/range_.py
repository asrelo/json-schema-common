from collections.abc import Sequence

from ._common import FormatCheckingFuncInfo

__all__ = (
    'is_numbers_range',
    'is_numbers_range_info',
)

def is_numbers_range(instance):
    return (
        isinstance(instance, Sequence)
        and (len(instance) == 2)
        and (instance[0] <= instance[1])
    )

is_numbers_range_info = FormatCheckingFuncInfo('numbers-range', is_numbers_range, (TypeError,))
