"""Syscall Package.

NOTE: If you add a new file/module to this package *YOU MUST*
import the file to `dashmips/__init__.py`
"""
from typing import Dict, Callable

from .Syscall import Syscall
from ..models import MipsProgram

Syscalls: Dict[int, Syscall] = {}


def mips_syscall(number: int):
    """Make a Syscall object from decorated function."""

    def decorator(function: Callable[[MipsProgram], None]) -> Syscall:
        """Syscall Decorator wrapper."""
        syscall = Syscall(function, number)
        Syscalls[syscall.number] = syscall
        return syscall

    return decorator
