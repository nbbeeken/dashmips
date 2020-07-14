"""Syscalls for reading from stdin."""
import os

from ..models import MipsProgram
from ..utils import bytesify, intify
from . import mips_syscall


@mips_syscall(5)
def read_int(program: MipsProgram):
    """Read Int from stdin. $v0 contains result."""
    user_input = input("")
    try:
        program.registers["$v0"] = int(user_input, 10)
    except ValueError:
        print("Not a parsable int")


@mips_syscall(8)
def read_str(program: MipsProgram):
    """Read Str from stdin. $a0 = address of input buffer $a1 = maximum number of characters to read."""
    user_input = input("")
    truncated_user_input = user_input[: program.registers["$a1"]]
    address = program.registers["$a0"]
    for offset, byte in enumerate(bytesify(truncated_user_input)):
        program.memory.write08(address + offset, bytes(byte))


@mips_syscall(12)
def read_char(program: MipsProgram):
    """Read Str from stdin. $a0 = address of input buffer $a1 = maximum number of characters to read."""
    user_input = os.read(0, 1)
    program.registers["$v0"] = intify(user_input)
