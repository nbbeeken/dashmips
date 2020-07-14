"""Mips Management."""
import inspect
from importlib import import_module
from typing import Callable, Dict

from .hardware import Memory

Directives: Dict[str, Callable[[str, Memory], int]] = {
    name.replace("directive_", ""): fn
    for name, fn in inspect.getmembers(import_module(".directives", "dashmips"), inspect.isfunction)
    if name.startswith("directive_")
}


class RE:
    """All Mips Regexs encapsulated in a class."""

    DATA_SEC = ".data"
    TEXT_SEC = ".text"

    REGISTER = r"(?:\$(?:(?:0|t[0-9]|s[0-7]|v[0-1]|a[0-3])|zero|sp|fp|gp|ra))"
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

    NUMBER = f"(?:{'|'.join(NUMBERS)})"

    ALL = {
        "register": REGISTER,
        "label": LABEL,
        "number": NUMBER,
        "instr_gap": INSTRGAP,
        "args_gap": ARGSGAP,
    }
