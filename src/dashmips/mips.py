"""Mips Management."""
import inspect
from typing import Any, Callable, Dict

import dashmips.directives as directives
from dashmips.hardware import Memory


class MipsException(Exception):
    """Mips related errors."""

    def __init__(self, message: str) -> None:
        """Create MipsException."""
        super().__init__(message)
        self.message = message


Directives: Dict[str, Callable[[str, Any, Memory], int]] = {
    directive.replace("_", ""): fn
    for directive, fn in inspect.getmembers(directives, inspect.isfunction)
}


class RE:
    """All Mips Regexs encapsulated in a class."""

    DATA_SEC = ".data"
    TEXT_SEC = ".text"

    REGISTER = (
        r"hi|lo|(?:\$(?:(?:0|t[0-9]|s[0-7]|v[0-1]|a[0-3])" +
        r"|zero|sp|fp|gp|ra))"
    )
    LABEL = r"\b[\w]+\b"
    DIRECTIVE = "\\." + "|\\.".join(Directives.keys())

    MACRO = r"\.macro\s+(\w+)\s*(?:\((.+)\))?"
    END_MACRO = r"\.end_macro"
    EQVS = r"\.eqv\s+(\w+)\s+(.+)"

    COMMENT = r"\#.*"

    INSTRGAP = r"\s+"
    ARGSGAP = r"\s*,\s*"

    # FIXME: Cannot capture '\''
    ASCII_LITERAL = r"'(?:[\x00-\x7F]|\\[0abfnrt\\ve])'"

    DEC = r"(?:(?:\+|-)?)(?:(?:[1-9](?:_?[0-9])*)|(?:0(?:_?0)*))"
    BIN = r"\b(?:0(?:b|B)(?:_?[0-1])+)\b"
    OCT = r"\b(?:0(?:o|O)(?:_?[0-7])+)\b"
    HEX = r"\b(?:0[xX])(?:_?[0-9a-fA-F])+\b"

    NUMBERS = [HEX, BIN, OCT, DEC, ASCII_LITERAL]

    NUMBER = "(?:" + "|".join(NUMBERS) + ")"

    ALL = {
        "register": REGISTER,
        "label": LABEL,
        "number": NUMBER,
        "instr_gap": INSTRGAP,
        "args_gap": ARGSGAP,
    }
