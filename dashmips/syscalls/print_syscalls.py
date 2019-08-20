"""Syscalls related to printing."""
from . import mips_syscall
from ..models import MipsProgram


@mips_syscall(4)
def print_string(program: MipsProgram):
    """Print string at address provided in $a0.

    :param program:
    """
    address = program.registers["$a0"]
    bin_string = []
    offset = 0
    while True:
        byte = program.memory[address + offset]
        if not byte:
            # null terminator encountered
            break
        bin_string.append(byte)
        offset += 1

    string = "".join([chr(c) for c in bin_string])
    print(string, end="")


@mips_syscall(11)
def print_char(program: MipsProgram):
    """Print string at address provided in $a0.

    :param program:
    """
    character = chr(program.registers["$a0"] & 0xFF)
    print(character, end="")


@mips_syscall(5)
def read_int(program: MipsProgram):
    """Read Int from stdin.

    :param program:
    """
    user_in = input("")
    try:
        program.registers["$v0"] = int(user_in, 10)
    except ValueError:
        print("Not a parsable int")


@mips_syscall(1)
def print_int(program: MipsProgram):
    """Print Int.

    :param program:
    """
    print(program.registers["$a0"], end="")


@mips_syscall(34)
def print_hex_int(program: MipsProgram):
    """Print Int in Hex.

    :param program:
    """
    print(f"0x{program.registers['$a0']:08x}", end="")


@mips_syscall(10)
def _exit(program: MipsProgram):
    """Exit MIPS Program.

    :param program:
    """
    # Internal definition of exited program
    program.exited = True


@mips_syscall(45)
def dump_program(program: MipsProgram):
    """Print json format of program.

    :param program:
    """
    import json

    print(json.dumps(program.to_dict(), indent=4))
