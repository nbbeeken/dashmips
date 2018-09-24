"""MipsProgram class."""
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class MipsProgram:
    """All data associated with a mips program."""

    from dashmips.preprocessor import Label
    from dashmips.hw import Memory, Registers
    name: str
    labels: Dict[str, Label]  # named tuple for labels
    code: List[str]
    memory: Memory
    registers: Registers

    @staticmethod
    def from_json(**kwargs):
        """Return Label for use in json.load."""
        if not all(
            key in kwargs
            for key in MipsProgram.__dataclass_fields__.keys()
        ):
            # Missing fields necessary for MipsProgram
            return None

        return MipsProgram(
            name=kwargs['name'],
            labels={name: Label(**label) for name, label in kwargs['labels']},
            code=kwargs['code'],
            memory=Memory(kwargs['memory']),
            registers=Registers(kwargs['registers']),
        )


class MipsException(Exception):
    """Exception specifically for mips errors."""

    pass
