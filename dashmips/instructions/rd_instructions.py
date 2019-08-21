"""Instructions that operate on one register."""
from typing import Tuple

from . import mips_instruction
from ..models import MipsProgram

PATTERN = r"{instr_gap}({register})"


def parse(args: Tuple[str, str, str]) -> Tuple[str]:
    """Parser for single register instructions."""
    return (args[2],)


@mips_instruction(PATTERN, parse)
def mflo(program: MipsProgram, rd: str):
    """Move from lo register to Reg[rd]."""
    program.registers[rd] = program.registers["lo"]


@mips_instruction(PATTERN, parse)
def mfhi(program: MipsProgram, rd: str):
    """Move from hi register to Reg[rd]."""
    program.registers[rd] = program.registers["hi"]


@mips_instruction(PATTERN, parse)
def mthi(program: MipsProgram, rd: str):
    """Move to hi register from Reg[rd]."""
    program.registers["hi"] = program.registers[rd]


@mips_instruction(PATTERN, parse)
def mtlo(program: MipsProgram, rd: str):
    """Move to lo register from Reg[rd]."""
    program.registers["lo"] = program.registers[rd]
