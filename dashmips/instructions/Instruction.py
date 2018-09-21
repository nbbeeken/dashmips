"""Instruction class."""
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
        self.parser = parser

    def __call__(self, registers, labels, memory, code, args=tuple()):
        """Callable Instruction."""
        return self.fn(registers, labels, memory, code, *args)

    def __repr__(self):
        """Return Representation string."""
        return f"Instruction({self.name})"
