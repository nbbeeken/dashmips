"""Syscalls for accessing files."""
import os

from . import mips_syscall
from ..utils import intify
from ..models import MipsProgram


@mips_syscall(13)
def open_file(program: MipsProgram):
    """Open file.

    $a0 = address of null-terminated string containing filename
    $a1 = flags
    https://docs.python.org/3/library/os.html#os.open
    """
    filename = program.memory.read_str(program.registers["$a0"])
    flags = program.registers["$a1"]
    # mode = program.registers["$a2"]
    try:
        program.registers["$v0"] = os.open(filename, flags)
    except FileNotFoundError as ex:
        print(ex)
        program.registers["$v0"] = -1  # TODO: This should be an E* value


@mips_syscall(14)
def read_file(program: MipsProgram):
    """Read from file.

    $a0 = file descriptor
    $a1 = address of input buffer
    $a2 = n bytes to read
    https://docs.python.org/3/library/os.html#os.read
    """
    fd = program.registers["$a0"]
    address = program.registers["$a1"]
    n = program.registers["$a2"]

    data_in = os.read(fd, n)
    program.memory.write_str(address, data_in)
    program.registers["$v0"] = len(data_in)


@mips_syscall(15)
def write_file(program: MipsProgram):
    """Write to file.

    $a0 = file descriptor
    $a1 = address of input buffer
    $a2 = n bytes to read
    https://docs.python.org/3/library/os.html#os.write
    """
    fd = program.registers["$a0"]
    address = program.registers["$a1"]
    n = program.registers["$a2"]

    data_out = bytes([intify(program.memory.read08(address + offset)) for offset in range(0, n)])
    written = os.write(fd, data_out)
    program.registers["$v0"] = written


@mips_syscall(16)
def close_file(program: MipsProgram):
    """Close file.

    $a0 = file descriptor
    https://docs.python.org/3/library/os.html#os.close
    """
    fd = program.registers["$a0"]

    os.close(fd)
    program.registers["$v0"] = 0
