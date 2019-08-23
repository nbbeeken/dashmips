"""Special Instructions."""
from typing import Tuple

from . import mips_instruction
from ..utils import MipsException
from ..models import MipsProgram
from ..syscalls import Syscalls


def parse(arg: Tuple[str, str]):
    """Instructions that take no arguments."""
    return tuple()


@mips_instruction("", parse)
def nop(program: MipsProgram):
    """Do nothing."""
    pass


@mips_instruction("", parse)
def syscall(program: MipsProgram):
    """Call syscall specified in $v0."""
    try:
        return Syscalls[program.registers["$v0"]](program)
    except KeyError:
        raise MipsException(f"Unsupported syscall {program.registers['$v0']}")
