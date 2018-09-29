"""Syscall Package.

NOTE: If you add a new file/module to this package *YOU MUST*
import the file to `dashmips/__init__.py`
"""
from typing import Dict

from dashmips.syscalls.Syscall import Syscall

Syscalls: Dict[int, Syscall] = {}


def mips_syscall(number):
    """Make a Syscall object from decorated function.

    Note: If you use this to make a new instruction
    YOU MUST import that function in `dashmips/__init__.py`
    """
    def decorator(function):
        syscall = Syscall(function, number)
        Syscalls[syscall.number] = syscall
        return syscall

    return decorator
