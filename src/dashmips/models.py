"""Data Models Essential to the Dashmips Ecosystem."""
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any

names_enum = tuple(
    enumerate(
        (
            # fmt: off
            "$zero",
            "$at",
            "$v0", "$v1",
            "$a0", "$a1", "$a2", "$a3",
            "$t0", "$t1", "$t2", "$t3", "$t4", "$t5", "$t6", "$t7",
            "$s0", "$s1", "$s2", "$s3", "$s4", "$s5", "$s6", "$s7",
            "$t8", "$t9",
            "$k0", "$k1",
            "$gp", "$sp", "$fp", "$ra",
            "pc",
            "hi",
            "lo",
            # fmt: on
        )
    )
)


def default_registers() -> Dict[str, int]:
    """Construct Default Registers."""
    return {name: 0 for i, name, in names_enum}


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
    memory: bytearray = field(default_factory=bytearray)
    registers: Dict[str, int] = field(default_factory=default_registers)
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
