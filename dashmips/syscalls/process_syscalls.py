"""Syscalls that manage a processes internals."""

from . import mips_syscall
from ..models import MipsProgram
from ..hardware import Memory


@mips_syscall(9)
def sbrk(program: MipsProgram):
    """Allocate heap space. $a0 = number of bytes to allocate  $v0 contains address of allocated memory."""
    num_bytes = (program.registers["$a0"] + 7) & (-8)  # Round to closest multiple of 8
    heap_size = program.registers["end_heap"] - (0 if program.registers["end_heap"] == 0 else program.memory.ram["heap"]["start"]) + num_bytes
    num_pages = (heap_size // Memory.PAGE_SIZE) + (1 if program.registers["end_heap"] == 0 else 0)
    if num_pages:
        address = program.memory.extend_heap(bytes([ord("@")] * (num_pages * Memory.PAGE_SIZE)))
    else:
        address = program.registers["end_heap"]
    program.registers["end_heap"] += num_bytes if program.registers["end_heap"] else address + num_bytes
    program.registers["$v0"] = address
