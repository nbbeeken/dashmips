"""Instruction class."""
from typing import Callable, Any, Iterable, Match

import dashmips.mips as mips
from dashmips.preprocessor import MipsProgram


class Instruction:
    """Instruction Class, callable."""

    def __init__(self, fn, regex_ptrn, parser):
        """
        Regex and argument parser for instruction.

        Adds itself to list upon instanciation.
        """
        self.fn: Callable[[MipsProgram, Iterable[Any]]] = fn

        name = self.fn.__name__
        if name.startswith('_'):
            name = name[1:]
        self.name = name

        self.regex = f"({self.name}){regex_ptrn}".format(**mips.RE.ALL)
        self.parser: Callable[[Match], Iterable[Any]] = parser

    def __call__(self, program: MipsProgram, args: Iterable = None):
        """Callable Instruction."""
        if not args:
            args = tuple()

        save_pc = program.registers['pc']
        program.registers['pc'] = None
        self.fn(program, *args)
        if program.registers['pc'] is None:
            # if not jmp/branch instruction pc will be None so we increment
            # otherwise, pc will have some value for next line of execution
            program.registers['pc'] = save_pc + 1

    def __repr__(self):
        """Return Representation string."""
        return f"Instruction({self.name})"
