"""Data Models Essential to the Dashmips Ecosystem."""
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any

from .hardware import Memory, Registers

@dataclass
class SourceLine:
    """Mips Preprocessor Label."""

    __slots__ = ("filename", "lineno", "line")

    filename: str
    lineno: int
    line: str


@dataclass
class Label:
    """Mips Preprocessor Label."""

    __slots__ = ("location", "kind", "value", "name")

    location: str
    kind: str
    value: int
    name: str


@dataclass
class MipsProgram:
    """All data associated with a mips program."""

    __slots__ = ("name", "filenames", "labels", "source", "__dict__")

    name: str
    filenames: List[str]
    labels: Dict[str, Label]
    source: List[SourceLine]
    memory: Memory = field(default_factory=Memory)
    registers: Registers = field(default_factory=Registers)
    eqvs: Dict[str, str] = field(default_factory=dict)
    exited: bool = False

    @staticmethod
    def from_dict(prg: Dict[str, Any]) -> "MipsProgram":
        """From Basic dictionary to MipsProgram.

        :param prg:
        """
        prg["memory"] = bytearray().fromhex(prg["memory"])
        # prg["registers"] = check_registers(prg["registers"])
        prg["labels"] = {ln: Label(**l) for ln, l in prg["labels"].items()}
        prg["source"] = [SourceLine(**m) for m in prg["source"]]
        return MipsProgram(**prg)

    def to_dict(self) -> Dict[str, Any]:
        """Two item iterable for dictionary making."""
        program_dict = asdict(self)
        program_dict["memory"] = program_dict["memory"].hex()
        return program_dict

    @property
    def current_line(self) -> SourceLine:
        """Return Current Line According to PC."""
        pc: int = self.registers["pc"]
        return self.source[pc]
