"""MipsProgram class."""
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class MipsProgram:
    """All data associated with a mips program."""

    from dashmips.preprocessor import Label
    from dashmips.hw import Memory, Registers
    labels: Dict[str, Label]
    code: List[str]
    memory: Memory
    registers: Registers


class MipsException(Exception):
    """Exception specifically for mips errors."""

    pass
