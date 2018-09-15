"""Mips Management."""
from typing import *


def directive(directive):
    """Derective handling master function."""
    def align(data):
        return None

    def asciiz(data):
        return (data[1:-1] + '\0').encode()

    def ascii(data):
        return (data[1:-1]).encode()

    def byte(data):
        return None

    def double(data):
        return None

    def end_macro(data):
        return None

    def eqv(data):
        return None

    def extern(data):
        return None

    def globl(data):
        return None

    def half(data):
        return None

    def include(data):
        return None

    def macro(data):
        return None

    def set(data):
        return None

    def space(data):
        return None

    def word(data):
        return None

directive_names: List[str] = []
# directive_names = [fn.name for fn in
#                    ast.walk(ast.parse(inspect.getsource(directive)))
#                    if type(fn).__name__ == 'FunctionDef'
#                    and fn.name is not 'directive']

Mips_Instructions = []


class Instruction:
    """Instruction Class, callable."""

    def __init__(self, regex, parser):
        """
        Regex and argument parser for instruction.

        Adds itself to list upon instanciation.
        """
        self.regex = regex
        self.parser = parser
        Mips_Instructions.append(self)

    def __call__(self, fn):
        """Callable Instruction."""
        self.name = fn.__name__
        if self.name.startswith('_'):
            self.name = self.name[1:]
        return fn


RE_REGISTER = (r"hi|lo|(?:\$(?:(?:t[0-9]|s[0-7]|v[0-1]|a[0-3])" +
               r"|zero|sp|fp|gp|ra))")
RE_LABEL = r"[a-zA-Z_][a-zA-Z0-9_]*"
RE_DIRECTIVE = "\\" + "|\\".join(directive_names)

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
