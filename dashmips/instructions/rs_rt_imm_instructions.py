"""Two Register and Immediate instructions."""
from typing import Tuple

from . import mips_instruction
from ..models import MipsProgram
from ..utils import parse_int

PATTERN = r"{instr_gap}({register}){args_gap}({register}){args_gap}({number})"


def parse(arg: Tuple[str, str, str, str, str]) -> Tuple[str, str, int]:
    """Two Register and Immediate instructions Parser."""
    return (arg[2], arg[3], parse_int(arg[4]))


@mips_instruction(PATTERN, parse)
def addi(program: MipsProgram, rs: str, rt: str, num: int):
    """Add immediate Reg[rs] = Reg[rt] + immediate."""
    program.registers[rs] = program.registers[rt] + num


@mips_instruction(PATTERN, parse)
def addiu(program: MipsProgram, rs: str, rt: str, num: int):
    """Add immediate unsigned Reg[rs] = Reg[rt] + immediate."""
    program.registers[rs] = (abs(program.registers[rt]) + abs(num)) & 0xFFFF_FFFF


@mips_instruction(PATTERN, parse)
def ori(program: MipsProgram, rs: str, rt: str, num: int):
    """Or immediate Reg[rs] = Reg[rt] | immediate."""
    program.registers[rs] = program.registers[rt] | num


@mips_instruction(PATTERN, parse)
def andi(program: MipsProgram, rs: str, rt: str, num: int):
    """And immediate Reg[rs] = Reg[rt] & immediate."""
    program.registers[rs] = program.registers[rt] & num


@mips_instruction(PATTERN, parse)
def slti(program: MipsProgram, rs: str, rt: str, num: int):
    """Set on less than immediate."""
    if program.registers[rt] < num:
        program.registers[rs] = 1
    else:
        program.registers[rs] = 0


@mips_instruction(PATTERN, parse)
def sltiu(program: MipsProgram, rs: str, rt: str, num: int):
    """Set on less than immediate unsigned."""
    if abs(program.registers[rt]) < abs(num):
        program.registers[rs] = 1
    else:
        program.registers[rs] = 0


@mips_instruction(PATTERN, parse)
def xori(program: MipsProgram, rs: str, rt: str, num: int):
    """Xor immediate Reg[rs] = Reg[rt] ^ immediate."""
    program.registers[rs] = program.registers[rt] ^ num


@mips_instruction(PATTERN, parse)
def sra(program: MipsProgram, rd: str, rs: str, num: int):
    """Shift Right Arithmetic."""
    msb = program.registers[rs] & 0x8000_0000
    program.registers[rd] = program.registers[rs] >> num
    program.registers[rd] |= msb


@mips_instruction(PATTERN, parse)
def sll(program: MipsProgram, rd: str, rt: str, num: int):
    """Shift Left Logical."""
    program.registers[rd] = (program.registers[rt] << num) & 0xFFFF_FFFF


@mips_instruction(PATTERN, parse)
def srl(program: MipsProgram, rd: str, rt: str, num: int):
    """Shift Right Logical."""
    program.registers[rd] = (program.registers[rt] >> num) & 0xFFFF_FFFF
