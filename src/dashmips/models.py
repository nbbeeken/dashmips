"""Data Models Essential to the Dashmips Ecosystem."""
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Tuple, TextIO, Iterable, Any, Optional, cast


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

    from dashmips.hardware import Memory, Registers

    __slots__ = ("name", "labels", "source", "__dict__")

    name: str
    labels: Dict[str, Label]
    source: List[SourceLine]
    memory: Memory = field(default_factory=Memory)
    registers: Registers = field(default_factory=Registers)
    eqvs: Dict[str, str] = field(default_factory=dict)

    @staticmethod
    def from_dict(prg: Dict[str, Any]) -> "MipsProgram":
        """From Basic dictionary to MipsProgram.

        :param prg:        """
        from dashmips.hardware import Memory, Registers

        prg["memory"] = Memory(prg["memory"])
        prg["registers"] = Registers(prg["registers"])
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

    __slots__ = ("command", "program", "__dict__")

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
        from dashmips.debugger import Commands

        if not payload:
            # Payload is Falsey
            return None
        if "command" not in payload:
            # There is no command to handle
            return None
        if payload["command"] not in Commands:
            # The command does not exist
            return None

        if "program" in payload:
            payload["program"] = MipsProgram.from_dict(
                payload.get("program", {}))
        else:
            payload["program"] = None
        return DebugMessage(**payload)


@dataclass
class Client:
    """A Client for DebugServer."""

    __slots__ = ("rfile", "wfile", "address")

    rfile: TextIO
    wfile: TextIO
    address: Tuple[str, int]
