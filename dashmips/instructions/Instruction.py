"""Instruction class."""
from typing import Callable, Tuple, Match
from dashmips.MipsProgram import MipsProgram
import dashmips.mips as mips


class Instruction:
    """Instruction Class, callable."""

    def __init__(self, fn, regex_ptrn, parser):
        """
        Regex and argument parser for instruction.

        Adds itself to list upon instanciation.
        """
        self.fn = fn

        name = self.fn.__name__
        if name.startswith('_'):
            name = name[1:]
        self.name = name

        self.regex = f"({self.name}){regex_ptrn}".format(**mips.RE.ALL)
        self.parser: Callable[[Union[Tuple, Match]], Tuple] = parser

    def __call__(self, program: MipsProgram, args=tuple()):
        """Callable Instruction."""
        return self.fn(program, *args)

    def __repr__(self):
        """Return Representation string."""
        return f"Instruction({self.name})"
