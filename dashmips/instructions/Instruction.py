"""Instruction class."""
from typing import Any, Iterable

from ..mips import RE
from ..models import MipsProgram
from ..utils import MipsException


class Instruction:
    """Instruction Class, callable."""

    def __init__(self, fn, regex_pattern: str, parser, label: bool = False):
        """Regex and argument parser for instruction.

        Adds itself to list upon instantiation.
        """
        self.function = fn

        name = fn.__name__
        if name.startswith("_"):
            name = name[1:]
        self.name = name

        if fn.__doc__:
            self.description = fn.__doc__.split("\n")[0]
        else:
            self.description = ""

        self.label = label
        self.pattern = regex_pattern
        self.regex = f"({self.name}){regex_pattern}".format(**RE.ALL)
        self.parser = parser

    def __call__(self, program: MipsProgram, args: Iterable[Any] = tuple()):
        """Callable Instruction."""
        try:
            self.function(program, *args)
        except KeyError as err:
            raise MipsException(f"Symbol {err} not found in symbol table")
        program.registers["pc"] += 1

    def __repr__(self) -> str:
        """Return Representation string."""
        return f"Instruction({self.name})"
