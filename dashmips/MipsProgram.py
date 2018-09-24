"""MipsProgram class."""
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class MipsProgram:
    """All data associated with a mips program."""

    from dashmips.preprocessor import Label
    from dashmips.hw import Memory, Registers
    name: str
    labels: Dict[str, Label]
    code: List[str]
    memory: Memory
    registers: Registers

    def to_dict(self, *include):
        """Mips Program to Dictionary."""
        if len(include) == 0:
            return {
                'name': self.name,
                'labels': self.labels,
                'code': self.code,
                'memory': self.memory,
                'registers': self.registers.to_regname_to_val_dict()
            }
        else:
            return {prop: self.__dict__[prop] for prop in include}


class MipsException(Exception):
    """Exception specifically for mips errors."""

    pass
