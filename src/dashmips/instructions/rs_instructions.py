"""Single Register insructions."""
from typing import Tuple, cast

from dashmips.instructions import mips_instruction
from dashmips.models import MipsProgram


PTRN = r"{instr_gap}({register})"


def parse(arg: Tuple[str, str, str]) -> Tuple[str]:
    """Single Register instruction parser.

    :param arg:
    """
    return (arg[2],)


@mips_instruction(PTRN, parse)
def jr(program: MipsProgram, rs: str) -> None:
    """Jump to address in Reg[rs].

    :param program:
    :param rs:
    """
    program.registers["pc"] = program.registers[rs]
