"""Syscalls that manage a processes internals."""

from . import mips_syscall
from ..models import MipsProgram
from ..hardware import Memory


@mips_syscall(9)
def sbrk(program: MipsProgram):
    """Allocate heap space."""
    num_bytes = program.registers["$a0"]
    num_pages = (num_bytes // Memory.PAGE_SIZE) + (0 if num_bytes % Memory.PAGE_SIZE == 0 else 1)
    address = program.memory.extend_heap(bytes([ord("@")] * (num_pages * Memory.PAGE_SIZE)))
    program.registers["$v0"] = address
