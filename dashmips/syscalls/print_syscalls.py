"""Syscalls related to printing."""
from . import mips_syscall
from ..models import MipsProgram
from ..utils import intify, bytesify
from struct import Struct


@mips_syscall(4)
def print_string(program: MipsProgram):
    """Print string. $a0 = address of null-terminated string to print."""
    address = program.registers["$a0"]
    string = program.memory.read_str(address)
    print(string, end="")


@mips_syscall(11)
def print_char(program: MipsProgram):
    """Print character. $a0 = character to print."""
    character = chr(program.registers["$a0"] & 0xFF)
    if ord(" ") <= ord(character) <= ord("~") or character in ("\n", "\t", "\r"):
        # is printable
        print(character, end="")


@mips_syscall(1)
def print_int(program: MipsProgram):
    """Print Int in Dec. $a0 = integer to print."""
    print(program.registers["$a0"], end="")


@mips_syscall(34)
def print_hex(program: MipsProgram):
    """Print Int in Hex. $a0 = integer to print."""
    print(f"0x{program.registers['$a0'] & 0xFFFFFFFF:08x}", end="")


@mips_syscall(35)
def print_bin(program: MipsProgram):
    """Print Int in Binary. $a0 = integer to print."""
    print(f"0b{program.registers['$a0'] & 0xFFFFFFFF:032b}", end="")


@mips_syscall(36)
def print_unsigned(program: MipsProgram):
    """Print Int as Unsigned. $a0 = integer to print."""
    print(f"{program.registers['$a0'] if program.registers['$a0'] > 0 else program.registers['$a0'] + 2**32}", end="")


@mips_syscall(37)
def print_ascii(program: MipsProgram):
    """Print Word in Ascii. $a0 = word to print."""
    ascii_string = repr(bytesify(program.registers["$a0"] & 0xFFFFFFFF)).replace("\\x00", "\\0")[2:-1]
    print(f"{ascii_string}", end="")


@mips_syscall(10)
def _exit(program: MipsProgram):
    """Exit MIPS Program."""
    # Internal definition of exited program
    program.exited = True


@mips_syscall(45)
def dump_program(program: MipsProgram):
    """Print json format of program."""
    import json

    print(json.dumps(program.to_dict(), indent=4), end="")
