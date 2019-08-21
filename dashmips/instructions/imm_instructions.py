"""Instructions that accept a label as an argument."""
from typing import Tuple

from . import mips_instruction
from ..models import MipsProgram

PATTERN = r"{instr_gap}({label})"


def parse(args: Tuple[str, str, str]) -> Tuple[str]:
    """Parse label to pass to instruction function."""
    return (args[2],)


@mips_instruction(PATTERN, parse, label=True)
def j(program: MipsProgram, address: str):
    """Jump unconditionally to label."""
    program.registers["pc"] = program.labels[address].value - 1


@mips_instruction(PATTERN, parse, label=True)
def jal(program: MipsProgram, address: str):
    """Jump unconditionally to label and set $ra to current $pc."""
    program.registers["$ra"] = program.registers["pc"] + 1
    program.registers["pc"] = program.labels[address].value - 1
