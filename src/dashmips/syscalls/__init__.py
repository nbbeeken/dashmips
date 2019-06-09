"""Syscall Package.

NOTE: If you add a new file/module to this package *YOU MUST*
import the file to `dashmips/__init__.py`
"""
from typing import Dict, Callable

from dashmips.syscalls.Syscall import Syscall
from dashmips.models import MipsProgram

Syscalls: Dict[int, Syscall] = {}


def mips_syscall(number: int) -> Callable[
        [Callable[[MipsProgram], None]], Syscall]:
    """Make a Syscall object from decorated function.

    Note: If you use this to make a new instruction
    YOU MUST import that function in `dashmips/__init__.py`

    :param number:
    """
    def decorator(function: Callable[[MipsProgram], None]) -> Syscall:
        """Syscall Decorator wrapper.

        :param function:
        """
        syscall = Syscall(function, number)
        Syscalls[syscall.number] = syscall
        return syscall

    return decorator
