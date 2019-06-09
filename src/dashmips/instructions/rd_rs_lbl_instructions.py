"""Instuctions that operate on one register."""
from typing import Tuple, cast

from dashmips.instructions import mips_instruction
from dashmips.models import MipsProgram


PTRN = r"{instr_gap}({register}){args_gap}({register}){args_gap}({label})"


def parse(arg: Tuple[str, str, str, str, str]) -> Tuple[str, str, str]:
    """Two Register and Immediate instructions Parser.

    :param arg:
    """
    return (arg[2], arg[3], arg[4])


@mips_instruction(PTRN, parse)
def beq(program: MipsProgram, rs: str, rt: str, label: str) -> None:
    """Branch to label if Reg[rs] == Reg[rt].

    :param program:
    :param rt:
    :param rs:
    :param label:
    """
    if program.registers[rs] == program.registers[rt]:
        program.registers["pc"] = program.labels[label].value


@mips_instruction(PTRN, parse)
def bne(program: MipsProgram, rs: str, rt: str, label: str) -> None:
    """Branch to label if Reg[rs] != Reg[rt].

    :param program:
    :param rt:
    :param rs:
    :param label:
    """
    if program.registers[rs] != program.registers[rt]:
        program.registers["pc"] = program.labels[label].value
