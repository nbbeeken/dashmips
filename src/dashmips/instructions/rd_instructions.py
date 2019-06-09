"""Instuctions that operate on one register."""
from typing import Tuple, cast

from dashmips.instructions import mips_instruction
from dashmips.models import MipsProgram

PTRN = r"{instr_gap}({register})"


def parse(args: Tuple[str, str, str]) -> Tuple[str]:
    """Parser for single register instructions.

    :param args:
    """
    return (args[2],)


@mips_instruction(PTRN, parse)
def mflo(program: MipsProgram, rd: str) -> None:
    """Move from lo register to Reg[rd].

    :param program:
    :param rd:
    """
    program.registers[rd] = program.registers["lo"]


@mips_instruction(PTRN, parse)
def mfhi(program: MipsProgram, rd: str) -> None:
    """Move from hi register to Reg[rd].

    :param program:
    :param rd:
    """
    program.registers[rd] = program.registers["hi"]


@mips_instruction(PTRN, parse)
def mthi(program: MipsProgram, rd: str) -> None:
    """Move to hi register from Reg[rd].

    :param program:
    :param rd:
    """
    program.registers["hi"] = program.registers[rd]


@mips_instruction(PTRN, parse)
def mtlo(program: MipsProgram, rd: str) -> None:
    """Move to lo register from Reg[rd].

    :param program:
    :param rd:
    """
    program.registers["lo"] = program.registers[rd]
