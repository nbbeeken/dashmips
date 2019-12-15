"""Data Models Essential to the Dashmips Ecosystem."""
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any

from .hardware import Memory, Registers
from .utils import hexdump


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

    def to_dict(self) -> Dict[str, Any]:
        """Program object to simple dict."""
        memory_str = {
            "stack": hexdump(self.memory.ram["stack"]["m"], reverse_idx=True),
            "data": hexdump(self.memory.ram["data"]["m"]),
            "heap": hexdump(self.memory.ram["heap"]["m"]),
        }
        return {
            "name": self.name,
            "filenames": self.filenames,
            "labels": {n: asdict(l) for n, l in self.labels.items()},
            "source": [asdict(s) for s in self.source],
            "memory": memory_str,
            "registers": self.registers,
            "eqvs": self.eqvs,
            "exited": self.exited,
        }

    @property
    def current_line(self) -> SourceLine:
        """Return Current Line According to PC."""
        pc: int = self.registers["pc"]
        return self.source[pc]
