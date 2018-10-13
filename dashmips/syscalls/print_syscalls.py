"""Syscalls related to printing."""
from dashmips.syscalls import mips_syscall


@mips_syscall(4)
def print_string(program):
    """Print string at address provided in $a0.

    :param program:

    """
    address = program.registers['$a0']
    i = 0
    byte_arr = []
    value = program.memory[address + i]
    while value != 0:
        byte_arr.append(value)
        i += 1
        value = program.memory[address + i]
    print(''.join([chr(c) for c in byte_arr]), end='')


@mips_syscall(11)
def print_char(program):
    """Print string at address provided in $a0.

    :param program:

    """
    character = chr(program.registers['$a0'] & 0xFF)
    print(character, end='')


@mips_syscall(5)
def read_int(program):
    """Read Int from stdin.

    :param program:

    """
    user_in = input('')
    try:
        program.registers['$v0'] = int(user_in, 10)
    except ValueError:
        print('Not a parsable int')


@mips_syscall(1)
def print_int(program):
    """Print Int.

    :param program:

    """
    print(program.registers['$a0'], end='')


@mips_syscall(34)
def print_hex_int(program):
    """Print Int in Hex.

    :param program:

    """
    print(hex(program.registers['$a0']), end='')


@mips_syscall(10)
def _exit(program):
    """Exit MIPS Program.

    :param program:

    """
    # Internal definition of exited program
    program.registers['pc'] = -1


@mips_syscall(45)
def dump_program(program):
    """Print json format of program.

    :param program:

    """
    import json
    d = dict(program)
    print(json.dumps(d, indent=4))
