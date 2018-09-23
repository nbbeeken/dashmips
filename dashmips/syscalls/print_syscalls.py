"""Syscalls related to printing."""
from dashmips.syscalls import mips_syscall


@mips_syscall(4)
def print_string(program):
    """Print string at address provided in $a0."""
    address = program.registers['$a0']
    i = 0
    byte_arr = []
    value = program.memory[address + i]
    while value != 0:
        byte_arr.append(value)
        i += 1
        value = program.memory[address + i]
    print(''.join([chr(c) for c in byte_arr]), end='')


@mips_syscall(5)
def read_int(program):
    """Read Int from stdin."""
    user_in = input('')
    try:
        program.registers['$v0'] = int(user_in, 10)
    except ValueError:
        print('Not a parsable int')


@mips_syscall(1)
def print_int(program):
    """Print Int."""
    print(program.registers['$a0'], end='')


@mips_syscall(10)
def _exit(program):
    """Exit MIPS Program."""
    # print('\n--- Program Output End ---\n')
    print(program.registers.pretty_str())
    exit(program.registers['$a0'])
