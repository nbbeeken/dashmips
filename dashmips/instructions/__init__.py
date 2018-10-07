"""Instructions Package.

NOTE: If you add a new file/module to this package *YOU MUST*
import the file to `dashmips/__init__.py`
"""
from typing import Dict

from dashmips.instructions.Instruction import Instruction

Instructions: Dict[str, Instruction] = {}


def mips_instruction(pattern, parser, label=False):
    """Make an Instruction object from decorated function.

    :param pattern: param parser:
    :param parser:

    """
    def decorator(function):
        """Instruction Decorator wrapper.

        :param function:

        """
        instr = Instruction(function, pattern, parser, label=label)
        Instructions[instr.name] = instr
        return instr

    return decorator


def parse_int(int_str):
    """Take a python number literal and returns an int."""
    arg = eval(int_str)
    if type(arg) is str:
        arg = ord(arg)
    else:
        arg = int(arg)
    return arg
