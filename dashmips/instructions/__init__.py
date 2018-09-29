"""Instructions Package.

NOTE: If you add a new file/module to this package *YOU MUST*
import the file to `dashmips/__init__.py`
"""
from typing import Dict

from dashmips.instructions.Instruction import Instruction

Instructions: Dict[str, Instruction] = {}


def mips_instruction(pattern, parser):
    """Make an Instruction object from decorated function."""
    def decorator(function):
        instr = Instruction(function, pattern, parser)
        Instructions[instr.name] = instr
        return instr

    return decorator
