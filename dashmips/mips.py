"""Mips Management."""
from typing import List
import inspect
import instructions

import directives

MipsDirectives = {
    directive: fn
    for directive, fn in inspect.getmembers(directives, inspect.isfunction)
}

MipsInstructions = []


class Instruction:
    """Instruction Class, callable."""

    def __init__(self, regex, parser):
        """
        Regex and argument parser for instruction.

        Adds itself to list upon instanciation.
        """
        self.regex = regex
        self.parser = parser
        MipsInstructions.append(self)

    def __call__(self, fn):
        """Callable Instruction."""
        self.name = fn.__name__
        if self.name.startswith('_'):
            self.name = self.name[1:]
        return fn


RE_REGISTER = (r"hi|lo|(?:\$(?:(?:t[0-9]|s[0-7]|v[0-1]|a[0-3])" +
               r"|zero|sp|fp|gp|ra))")
RE_LABEL = r"[a-zA-Z_][a-zA-Z0-9_]*"
RE_DIRECTIVE = "\\." + "|\\.".join(MipsDirectives.keys())

RE_INSTRGAP = r"\s+"
RE_ARGSGAP = r"\s*,\s*"

RE_DEC = "(?:(?:+|-)?)(?:(?:[1-9](?:_?[0-9])*)|(?:0(?:_?0)*))"
RE_BIN = "(?:0(?:b|B)(?:_?[0-1])+)"
RE_OCT = "(?:0(?:o|O)(?:_?[0-7])+)"
RE_HEX = "(?:0(?:x|X)(?:_?([0-9]|[a-f]|[A-F]))+)"

RE_NUMBERS = [
    RE_DEC,
    RE_BIN,
    RE_OCT,
    RE_HEX,
]

RE_NUMBER = "(?:\d+)"  # "(?:" + "|".join(RE_NUMBERS) + ")"

REGEXS = {
    'register': RE_REGISTER,
    'label': RE_LABEL,
    'number': RE_NUMBER,
    'instr_gap': RE_INSTRGAP,
    'args_gap': RE_ARGSGAP,
}


def instr_re(i, p):
    """Instruction Regex Builder."""
    return f"({i}){p}".format(**REGEXS)
