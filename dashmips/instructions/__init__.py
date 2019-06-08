"""Instructions Package.

NOTE: If you add a new file/module to this package *YOU MUST*
import the file to `dashmips/__init__.py`
"""
from typing import Dict, Union, Callable, Tuple, Any, Iterable

from dashmips.instructions.Instruction import Instruction

Instructions: Dict[str, Instruction] = {}


def mips_instruction(
        pattern: str,
        parser: Callable,
        label: bool = False) -> Callable[[Callable], Instruction]:
    """Make an Instruction object from decorated function.

    :param pattern: param parser:
    :param parser:
    """
    def decorator(function: Callable) -> Instruction:
        """Instruction Decorator wrapper.

        :param function:
        """
        instr = Instruction(function, pattern, parser, label=label)
        Instructions[instr.name] = instr
        return instr

    return decorator


def parse_int(int_str: str) -> int:
    """Take a python number literal and returns an int."""
    arg: Union[int, str] = eval(int_str)

    if isinstance(arg, str):
        arg = int(ord(arg))
    else:
        arg = int(arg)

    return arg
