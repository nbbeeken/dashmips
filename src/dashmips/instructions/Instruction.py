"""Instruction class."""
from typing import Callable, Any, Iterable, Match, Tuple

import dashmips.mips as mips
from dashmips.models import MipsProgram


class Instruction:
    """Instruction Class, callable."""

    def __init__(
        self, fn: Callable, regex_ptrn: str,
        parser: Callable, label: bool = False,
    ) -> None:
        """
        Regex and argument parser for instruction.

        Adds itself to list upon instanciation.
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
        self.pattern = regex_ptrn
        self.regex = f"({self.name}){regex_ptrn}".format(**mips.RE.ALL)
        self.parser = parser

    def __call__(self, program: MipsProgram,
                 args: Iterable[Any] = tuple()) -> None:
        """Callable Instruction."""
        self.function(program, *args)
        if not program.registers.pc_changed:
            # if not jmp/branch instruction pc
            # wont have been changed in the instruction
            # otherwise, pc will have some value for next line of execution
            program.registers["pc"] += 1

        program.registers.pc_changed = False  # reset for next loop

    def __repr__(self) -> str:
        """Return Representation string."""
        return f"Instruction({self.name})"
