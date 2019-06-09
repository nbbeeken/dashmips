"""Register Immediate (label: str) instructions."""
from typing import Tuple, cast

from dashmips.instructions import mips_instruction
from dashmips.models import MipsProgram


PTRN = r"{instr_gap}({register}){args_gap}({label})"


def parse(arg: Tuple[str, str, str, str]) -> Tuple[str, str]:
    """Parser for reg imm insructions.

    :param arg:
    """
    return (arg[2], arg[3])


@mips_instruction(PTRN, parse, label=True)
def bgez(program: MipsProgram, rs: str, label: str) -> None:
    """Branch if Reg[rs] >= 0.

    :param program:
    :param label:
    :param rs:
    """
    if program.registers[rs] >= 0:
        program.registers["pc"] = program.labels[label].value


@mips_instruction(PTRN, parse, label=True)
def bgezal(program: MipsProgram, rs: str, label: str) -> None:
    """Branch if Reg[rs] >= 0 and link.

    :param program:
    :param label:
    :param rs:
    """
    if program.registers[rs] >= 0:
        program.registers["pc"] = program.labels[label].value


@mips_instruction(PTRN, parse, label=True)
def bgtz(program: MipsProgram, rs: str, label: str) -> None:
    """Branch if Reg[rs] > 0.

    :param program:
    :param label:
    :param rs:
    """
    if program.registers[rs] > 0:
        program.registers["pc"] = program.labels[label].value


@mips_instruction(PTRN, parse, label=True)
def blez(program: MipsProgram, rs: str, label: str) -> None:
    """Branch if Reg[rs] <= 0.

    :param program:
    :param label:
    :param rs:
    """
    if program.registers[rs] <= 0:
        program.registers["pc"] = program.labels[label].value


@mips_instruction(PTRN, parse, label=True)
def bltz(program: MipsProgram, rs: str, label: str) -> None:
    """Branch if Reg[rs] < 0.

    :param program:
    :param label:
    :param rs:
    """
    if program.registers[rs] < 0:
        program.registers["pc"] = program.labels[label].value


@mips_instruction(PTRN, parse, label=True)
def bltzal(program: MipsProgram, rs: str, label: str) -> None:
    """Branch if Reg[rs] < 0 and link.

    :param program:
    :param label:
    :param rs:
    """
    if program.registers[rs] < 0:
        program.registers["$ra"] = program.registers["pc"]
        program.registers["pc"] = program.labels[label].value
