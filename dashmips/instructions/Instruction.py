"""Instruction class."""
from typing import Callable, Any, Iterable, Match

import dashmips.mips as mips
from dashmips.preprocessor import MipsProgram


class Instruction:
    """Instruction Class, callable."""

    def __init__(self, fn, regex_ptrn, parser, label=False):
        """
        Regex and argument parser for instruction.

        Adds itself to list upon instanciation.
        """
        self.fn: Callable[[MipsProgram, Iterable[Any]]] = fn

        name = self.fn.__name__
        if name.startswith('_'):
            name = name[1:]
        self.name = name

        self.label = label
        self.pattern = regex_ptrn
        self.regex = f"({self.name}){regex_ptrn}".format(**mips.RE.ALL)
        self.parser: Callable[[Match], Iterable[Any]] = parser

    def __call__(self, program: MipsProgram, args: Iterable = None):
        """Callable Instruction."""
        if not args:
            args = tuple()

        self.fn(program, *args)
        if not program.registers.pc_changed:
            # if not jmp/branch instruction pc
            # wont have been changed in the instruction
            # otherwise, pc will have some value for next line of execution
            program.registers['pc'] += 1

        program.registers.pc_changed = False  # reset for next loop

    def __repr__(self):
        """Return Representation string."""
        return f"Instruction({self.name})"
