"""Mips Management."""
import inspect
from typing import Dict, Callable, Any

import dashmips.directives as directives
from dashmips.hardware import Memory


class MipsException(Exception):
    """Mips related errors."""

    def __init__(self, message):
        """Create MipsException."""
        super().__init__(message)
        self.message = message


Directives: Dict[str, Callable[[str, Any, Memory], int]] = {
    directive: fn
    for directive, fn in
    inspect.getmembers(directives, inspect.isfunction)
}


class RE:
    """All Mips Regexs encapsulated in a class."""

    DATA_SEC = ".data"
    TEXT_SEC = ".text"

    REGISTER = (r"hi|lo|(?:\$(?:(?:t[0-9]|s[0-7]|v[0-1]|a[0-3])" +
                r"|zero|sp|fp|gp|ra))")
    LABEL = r"[a-zA-Z_][a-zA-Z0-9_]*"
    DIRECTIVE = "\\." + "|\\.".join(Directives.keys())

    COMMENT = r"\#.*"

    INSTRGAP = r"\s+"
    ARGSGAP = r"\s*,\s*"

    DEC = "(?:(?:+|-)?)(?:(?:[1-9](?:_?[0-9])*)|(?:0(?:_?0)*))"
    BIN = "(?:0(?:b|B)(?:_?[0-1])+)"
    OCT = "(?:0(?:o|O)(?:_?[0-7])+)"
    HEX = "(?:0(?:x|X)(?:_?([0-9]|[a-f]|[A-F]))+)"

    NUMBERS = [
        DEC,
        BIN,
        OCT,
        HEX,
    ]

    NUMBER = "(?:\d+)"  # "(?:" + "|".join(RE_NUMBERS) + ")"

    ALL = {
        'register': REGISTER,
        'label': LABEL,
        'number': NUMBER,
        'instr_gap': INSTRGAP,
        'args_gap': ARGSGAP,
    }
