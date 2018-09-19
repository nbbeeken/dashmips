"""Syscalls related to printing."""
from dashmips.mips import mips_syscall


@mips_syscall(4)
def print_string(registers, labels, memory):
    """Print string at address provided in $a0."""
    print('WIP')


@mips_syscall(10)
def exit(registers, labels, memory):
    """Exit MIPS Program."""
    print('WIP PROPOGATE EXIT')
