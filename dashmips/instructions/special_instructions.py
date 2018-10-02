"""Special Instructions."""
from dashmips.instructions import mips_instruction
from dashmips.syscalls import Syscalls


def parse(arg):
    """Instructions that take no arguments."""
    return tuple()


@mips_instruction('', parse)
def nop(program):
    """Do nothing."""
    return True


@mips_instruction('', parse)
def syscall(program):
    """Call syscall specified in $v0."""
    return Syscalls[program.registers['$v0']](program)
