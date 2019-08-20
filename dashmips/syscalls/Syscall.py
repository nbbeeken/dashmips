"""Syscall Class."""
from typing import Callable

from ..models import MipsProgram


class Syscall:
    """Syscall Class, callable."""

    def __init__(self, function: Callable[[MipsProgram], None], number: int):
        """Create Syscall."""
        self.function = function
        if function.__doc__:
            self.description = function.__doc__.split("\n")[0]
        else:
            self.description = ""

        name = self.function.__name__
        if name.startswith("_"):
            name = name[1:]
        self.name = name
        self.number = number

    def __call__(self, program: MipsProgram):
        """Callable Instruction."""
        self.function(program)

    def __repr__(self) -> str:
        """Return Representation string."""
        return f"Syscall({self.number}, {self.name})"
