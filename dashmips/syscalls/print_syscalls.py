"""Syscalls related to printing."""
from dashmips.syscalls import mips_syscall
from dashmips.models import MipsProgram


@mips_syscall(4)
def print_string(program: MipsProgram) -> None:
    """Print string at address provided in $a0.

    :param program:
    """
    address = program.registers["$a0"]
    bstring = program.memory[address: program.memory.index(0x0, address)]
    string = "".join([chr(c) for c in bstring])
    print(string, end="")


@mips_syscall(11)
def print_char(program: MipsProgram) -> None:
    """Print string at address provided in $a0.

    :param program:
    """
    character = chr(program.registers["$a0"] & 0xFF)
    print(character, end="")


@mips_syscall(5)
def read_int(program: MipsProgram) -> None:
    """Read Int from stdin.

    :param program:
    """
    user_in = input("")
    try:
        program.registers["$v0"] = int(user_in, 10)
    except ValueError:
        print("Not a parsable int")


@mips_syscall(1)
def print_int(program: MipsProgram) -> None:
    """Print Int.

    :param program:
    """
    print(program.registers["$a0"], end="")


@mips_syscall(34)
def print_hex_int(program: MipsProgram) -> None:
    """Print Int in Hex.

    :param program:
    """
    print(hex(program.registers["$a0"]), end="")


@mips_syscall(10)
def _exit(program: MipsProgram) -> None:
    """Exit MIPS Program.

    :param program:
    """
    # Internal definition of exited program
    program.registers["pc"] = -1


@mips_syscall(45)
def dump_program(program: MipsProgram) -> None:
    """Print json format of program.

    :param program:
    """
    import json

    print(json.dumps(program.to_dict(), indent=4))
