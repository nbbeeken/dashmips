"""Register Immediate (label: str) instructions."""
from typing import Tuple

from . import mips_instruction
from ..models import MipsProgram

PATTERN = r"{instr_gap}({register}){args_gap}({label})"


def parse(arg: Tuple[str, str, str, str]) -> Tuple[str, str]:
    """Parser for reg imm insructions."""
    return (arg[2], arg[3])


@mips_instruction(PATTERN, parse, label=True)
def bgez(program: MipsProgram, rs: str, label: str):
    """Branch if Reg[rs] >= 0."""
    if program.registers[rs] >= 0:
        program.registers["pc"] = program.labels[label].value - 1


@mips_instruction(PATTERN, parse, label=True)
def bgezal(program: MipsProgram, rs: str, label: str):
    """Branch if Reg[rs] >= 0 and link."""
    if program.registers[rs] >= 0:
        program.registers["pc"] = program.labels[label].value - 1


@mips_instruction(PATTERN, parse, label=True)
def bgtz(program: MipsProgram, rs: str, label: str):
    """Branch if Reg[rs] > 0."""
    if program.registers[rs] > 0:
        program.registers["pc"] = program.labels[label].value - 1


@mips_instruction(PATTERN, parse, label=True)
def blez(program: MipsProgram, rs: str, label: str):
    """Branch if Reg[rs] <= 0."""
    if program.registers[rs] <= 0:
        program.registers["pc"] = program.labels[label].value - 1


@mips_instruction(PATTERN, parse, label=True)
def bltz(program: MipsProgram, rs: str, label: str):
    """Branch if Reg[rs] < 0."""
    if program.registers[rs] < 0:
        program.registers["pc"] = program.labels[label].value - 1


@mips_instruction(PATTERN, parse, label=True)
def bltzal(program: MipsProgram, rs: str, label: str):
    """Branch if Reg[rs] < 0 and link."""
    if program.registers[rs] < 0:
        program.registers["$ra"] = program.registers["pc"]
        program.registers["pc"] = program.labels[label].value - 1
