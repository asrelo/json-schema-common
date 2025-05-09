from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    from typing import Callable

class FormatCheckingFuncInfo(NamedTuple):
    format_: str
    func: 'Callable[[object], bool]'
    raises: type[Exception] | tuple[type[Exception], ...] = ()

def register_func_in_checker(checker, func_info):
    return checker.checks(func_info.format_, func_info.raises)(func_info.func)

def register_funcs_in_checkers(checker, funcs_info):
    return [register_func_in_checker(checker, func_info) for func_info in funcs_info]
