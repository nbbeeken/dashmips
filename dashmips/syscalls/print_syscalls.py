"""Syscalls related to printing."""
from dashmips.syscalls import mips_syscall


@mips_syscall(4)
def print_string(registers, labels, memory, code):
    """Print string at address provided in $a0."""
    address = registers['$a0']
    i = 0
    byte_arr = []
    value = memory[address + i]
    while value != 0:
        byte_arr.append(value)
        i += 1
        value = memory[address + i]
    print(''.join([chr(c) for c in byte_arr]))


@mips_syscall(10)
def _exit(registers, labels, memory, code):
    """Exit MIPS Program."""
    print('WIP PROPOGATE EXIT')
