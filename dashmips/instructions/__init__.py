"""Instructions Package.

NOTE: If you add a new file/module to this package *YOU MUST*
import the file to `dashmips/__init__.py`
"""

from .Instruction import Instruction

Instructions = {}


def mips_instruction(pattern: str, parser, label: bool = False):
    """Make an Instruction object from decorated function."""

    def decorator(function) -> Instruction:
        """Instruction Decorator wrapper."""
        instr = Instruction(function, pattern, parser, label=label)
        Instructions[instr.name] = instr
        return instr

    return decorator
