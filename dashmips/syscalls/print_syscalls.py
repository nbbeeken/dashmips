"""Syscalls related to printing."""
from . import mips_syscall
from ..models import MipsProgram
from ..utils import intify


@mips_syscall(4)
def print_string(program: MipsProgram):
    """Print string at address provided in $a0."""
    address = program.registers["$a0"]
    string = program.memory.read_str(address)
    print(string, end="")


@mips_syscall(11)
def print_char(program: MipsProgram):
    """Print string at address provided in $a0."""
    character = chr(program.registers["$a0"] & 0xFF)
    if ord(" ") <= ord(character) <= ord("~") or character in ("\n", "\t", "\r"):
        # is printable
        print(character, end="")


@mips_syscall(1)
def print_int(program: MipsProgram):
    """Print Int in Dec."""
    print(program.registers["$a0"], end="")


@mips_syscall(34)
def print_hex(program: MipsProgram):
    """Print Int in Hex."""
    print(f"{program.registers['$a0'] & 0xFFFFFFFF:08x}", end="")


@mips_syscall(35)
def print_bin(program: MipsProgram):
    """Print Int in Bin."""
    print(f"{program.registers['$a0'] & 0xFFFFFFFF:032b}", end="")


@mips_syscall(10)
def _exit(program: MipsProgram):
    """Exit MIPS Program."""
    # Internal definition of exited program
    program.exited = True


@mips_syscall(45)
def dump_program(program: MipsProgram):
    """Print json format of program."""
    import json

    print(json.dumps(program.to_dict(), indent=4))
