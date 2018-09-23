"""Special Instructions."""
from dashmips.instructions import mips_instruction
from dashmips.syscalls import Syscalls


def parse(arg):
    return tuple()


@mips_instruction('', parse)
def nop(program):
    return True


@mips_instruction('', parse)
def syscall(program):
    return Syscalls[program.registers['$v0']](program)
