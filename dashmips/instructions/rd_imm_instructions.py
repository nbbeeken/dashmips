"""Instructions that accept a register and immediate as an argument."""
from typing import Tuple

from . import mips_instruction
from ..models import MipsProgram
from ..utils import parse_int

PATTERN = r"{instr_gap}({register}){args_gap}({number})"


def parse(args: Tuple[str, str, str, str]) -> Tuple[str, int]:
    """Parse rd and imm to pass to instruction function."""
    return (args[2], parse_int(args[3]))


@mips_instruction(PATTERN, parse)
def lui(program: MipsProgram, rd: str, immediate: int):
    """Load upper bits from immediate."""
    program.registers[rd] = (immediate << 16) & 0xFFFF_0000
