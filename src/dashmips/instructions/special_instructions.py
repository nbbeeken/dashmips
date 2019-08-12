"""Special Instructions."""
from typing import Tuple, cast

from . import mips_instruction
from ..models import MipsProgram
from ..syscalls import Syscalls


def parse(arg: Tuple[str, str]):
    """Instructions that take no arguments.

    :param arg:
    """
    return tuple()


@mips_instruction("", parse)
def nop(program: MipsProgram):
    """Do nothing.

    :param program:
    """
    pass


@mips_instruction("", parse)
def syscall(program: MipsProgram):
    """Call syscall specified in $v0.

    :param program:
    """
    return Syscalls[program.registers["$v0"]](program)
