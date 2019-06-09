"""Special Instructions."""
from typing import Tuple, cast

from dashmips.instructions import mips_instruction
from dashmips.models import MipsProgram
from dashmips.syscalls import Syscalls


def parse(arg: Tuple[str, str]) -> Tuple:
    """Instructions that take no arguments.

    :param arg:
    """
    return tuple()


@mips_instruction("", parse)
def nop(program: MipsProgram) -> None:
    """Do nothing.

    :param program:
    """
    pass


@mips_instruction("", parse)
def syscall(program: MipsProgram) -> None:
    """Call syscall specified in $v0.

    :param program:
    """
    return Syscalls[program.registers["$v0"]](program)
