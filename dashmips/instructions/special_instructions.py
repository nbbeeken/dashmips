"""Special Instructions."""
from dashmips.instructions import mips_instruction
from dashmips.syscalls import Syscalls


def parse(arg):
    return tuple()


@mips_instruction('', parse)
def nop(registers, labels, memory, code):
    return True


@mips_instruction('', parse)
def syscall(registers, labels, memory, code):
    return Syscalls[registers['$v0']](registers, labels, memory, code)
