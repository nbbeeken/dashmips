"""Instructions that accept a register and immediate as an argument."""
from typing import Tuple, cast

from dashmips.instructions import mips_instruction, parse_int
from dashmips.models import MipsProgram

PTRN = r"{instr_gap}({register}){args_gap}({number})"


def parse(args: Tuple[str, str, str, str]) -> Tuple[str, int]:
    """Parse rd and imm to pass to instruction function.

    :param args:
    """
    return (args[2], parse_int(args[3]))


@mips_instruction(PTRN, parse)
def lui(program: MipsProgram, rd: str, immediate: int) -> None:
    """Load upper bits from immediate.

    :param program:
    :param rd:
    :param immediate:
    """
    program.registers[rd] = (immediate << 16) & 0xFFFF_0000
