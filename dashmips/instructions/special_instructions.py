"""Special Instructions."""
from dashmips.instructions import mips_instruction
from dashmips.syscalls import Syscalls


def parse(arg):
    return tuple()


@mips_instruction('', parse)
def nop(regs, lbls):
    return True


@mips_instruction('', parse)
def syscall(regs, lbls):
    return Syscalls[regs['$v0']](regs, lbls, [])
