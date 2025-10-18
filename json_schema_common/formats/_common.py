from collections.abc import Callable, Iterable, Sequence
from typing import TYPE_CHECKING, TypeAlias, TypeVar, NamedTuple

if TYPE_CHECKING:
    from jsonschema import FormatChecker


FormatCheckFn: TypeAlias = Callable[[object], bool]

F = TypeVar('F', bound=FormatCheckFn)


class FormatCheckingFuncInfo(NamedTuple):
    format_: str
    func: FormatCheckFn
    raises: type[Exception] | tuple[type[Exception], ...] = ()


def register_func_in_checker(
    checker: 'FormatChecker', func_info: FormatCheckingFuncInfo,
) -> FormatCheckFn:
    return checker.checks(func_info.format_, func_info.raises)(func_info.func)


def register_funcs_in_checker(
    checker: 'FormatChecker', funcs_info: Iterable[FormatCheckingFuncInfo],
) -> Sequence[FormatCheckFn]:
    return [register_func_in_checker(checker, func_info) for func_info in funcs_info]
