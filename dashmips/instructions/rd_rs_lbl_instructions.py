"""Instructions that operate on one register."""
from typing import Tuple

from . import mips_instruction
from ..models import MipsProgram

PATTERN = r"{instr_gap}({register}){args_gap}({register}){args_gap}({label})"


def parse(arg: Tuple[str, str, str, str, str]) -> Tuple[str, str, str]:
    """Two Register and Immediate instructions Parser."""
    return (arg[2], arg[3], arg[4])


@mips_instruction(PATTERN, parse)
def beq(program: MipsProgram, rs: str, rt: str, label: str):
    """Branch to label if Reg[rs] == Reg[rt]."""
    if program.registers[rs] == program.registers[rt]:
        program.registers["pc"] = program.labels[label].value - 1


@mips_instruction(PATTERN, parse)
def bne(program: MipsProgram, rs: str, rt: str, label: str):
    """Branch to label if Reg[rs] != Reg[rt]."""
    if program.registers[rs] != program.registers[rt]:
        program.registers["pc"] = program.labels[label].value - 1
