"""Data Models Essential to the Dashmips Ecosystem."""
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Tuple, TextIO, Iterable, Any, Optional, cast

names_enum = tuple(
    enumerate(
        (
            # fmt: off
            '$zero',
            '$at',
            '$v0', '$v1',
            '$a0', '$a1', '$a2', '$a3',
            '$t0', '$t1', '$t2', '$t3', '$t4', '$t5', '$t6', '$t7',
            '$s0', '$s1', '$s2', '$s3', '$s4', '$s5', '$s6', '$s7',
            '$t8', '$t9',
            '$k0', '$k1',
            '$gp', '$sp', '$fp', '$ra',
            'pc',
            'hi',
            'lo',
            # fmt: on
        )
    )
)


def default_registers() -> dict:
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

    from .hardware import Memory, Registers

    __slots__ = ("name", "labels", "source", "__dict__")

    name: str
    labels: Dict[str, Label]
    source: List[SourceLine]
    memory: bytearray = field(default_factory=bytearray)
    registers: Dict[str, int] = field(default_factory=default_registers)
    eqvs: Dict[str, str] = field(default_factory=dict)

    @staticmethod
    def from_dict(prg: Dict[str, Any]) -> "MipsProgram":
        """From Basic dictionary to MipsProgram.

        :param prg:
        """
        from .hardware import Memory, Registers

        prg["memory"] = Memory(prg["memory"])
        # prg["registers"] = check_registers(prg["registers"])
        prg["labels"] = {ln: Label(**l) for ln, l in prg["labels"].items()}
        prg["source"] = [SourceLine(**m) for m in prg["source"]]
        return MipsProgram(**prg)

    def to_dict(self) -> dict:
        """Two item iterable for dictionary making."""
        return asdict(self)

    @property
    def current_line(self) -> SourceLine:
        """Return Current Line According to PC."""
        pc: int = self.registers["pc"]
        return self.source[pc]


@dataclass
class DebugMessage:
    """Format for debug messages."""

    __slots__ = (
        "command", "program", "__dict__"
    )

    command: str
    program: MipsProgram
    breakpoints: List[int] = field(default_factory=list)
    message: str = ""
    error: bool = False

    def __post_init__(self) -> None:
        """Ensure unique breakpoints."""
        # set to remove duplicates and sort
        self.breakpoints = sorted(set(self.breakpoints))

    def to_dict(self) -> dict:
        """Make DebugMessage castable to dict."""
        return asdict(self)

    @staticmethod
    def from_dict(payload: dict) -> Optional["DebugMessage"]:
        """Deserialize from json to DebugMessage.

        :param payload:
        """
        from .debugger import COMMANDS

        if not payload:
            # Payload is Falsey
            return None
        if "command" not in payload:
            # There is no command to handle
            return None
        if payload["command"] not in COMMANDS:
            # The command does not exist
            return None

        if "program" in payload:
            payload["program"] = MipsProgram.from_dict(
                payload.get("program", {}))
        else:
            payload["program"] = None
        return DebugMessage(**payload)
