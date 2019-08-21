"""Single Register insructions."""
from typing import Tuple

from . import mips_instruction
from ..models import MipsProgram

PATTERN = r"{instr_gap}({register})"


def parse(arg: Tuple[str, str, str]) -> Tuple[str]:
    """Single Register instruction parser."""
    return (arg[2],)


@mips_instruction(PATTERN, parse)
def jr(program: MipsProgram, rs: str):
    """Jump to address in Reg[rs]."""
    program.registers["pc"] = program.registers[rs] - 1
