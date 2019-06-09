"""Two Register and Immediate instructions."""
from typing import Tuple, cast

from dashmips.instructions import mips_instruction, parse_int
from dashmips.models import MipsProgram

PTRN = r"{instr_gap}({register}){args_gap}({register}){args_gap}({number})"


def parse(arg: Tuple[str, str, str, str, str]) -> Tuple[str, str, int]:
    """Two Register and Immediate instructions Parser.

    :param arg:
    """
    return (arg[2], arg[3], parse_int(arg[4]))


@mips_instruction(PTRN, parse)
def addi(program: MipsProgram, rs: str, rt: str, num: int) -> None:
    """Add immediate Reg[rs] = Reg[rt] + immediate.

    :param program:
    :param rt:
    :param rs:
    :param num:
    """
    program.registers[rs] = program.registers[rt] + num


@mips_instruction(PTRN, parse)
def addiu(program: MipsProgram, rs: str, rt: str, num: int) -> None:
    """Add immediate unsigned Reg[rs] = Reg[rt] + immediate.

    :param program:
    :param rt:
    :param rs:
    :param num:
    """
    program.registers[rs] = (
        abs(program.registers[rt]) + abs(num)) & 0xFFFF_FFFF


@mips_instruction(PTRN, parse)
def ori(program: MipsProgram, rs: str, rt: str, num: int) -> None:
    """Or immediate Reg[rs] = Reg[rt] | immediate.

    :param program:
    :param rt:
    :param rs:
    :param num:
    """
    program.registers[rs] = program.registers[rt] | num


@mips_instruction(PTRN, parse)
def andi(program: MipsProgram, rs: str, rt: str, num: int) -> None:
    """And immediate Reg[rs] = Reg[rt] & immediate.

    :param program:
    :param rt:
    :param rs:
    :param num:
    """
    program.registers[rs] = program.registers[rt] & num


@mips_instruction(PTRN, parse)
def slti(program: MipsProgram, rs: str, rt: str, num: int) -> None:
    """Set on less than immediate.

    :param program:
    :param rt:
    :param rs:
    :param num:
    """
    if program.registers[rt] < num:
        program.registers[rs] = 1
    else:
        program.registers[rs] = 0


@mips_instruction(PTRN, parse)
def sltiu(program: MipsProgram, rs: str, rt: str, num: int) -> None:
    """Set on less than immediate unsigned.

    :param program:
    :param rt:
    :param rs:
    :param num:
    """
    if abs(program.registers[rt]) < abs(num):
        program.registers[rs] = 1
    else:
        program.registers[rs] = 0


@mips_instruction(PTRN, parse)
def xori(program: MipsProgram, rs: str, rt: str, num: int) -> None:
    """Xor immediate Reg[rs] = Reg[rt] ^ immediate.

    :param program:
    :param rt:
    :param rs:
    :param num:
    """
    program.registers[rs] = program.registers[rt] ^ num


@mips_instruction(PTRN, parse)
def sra(program: MipsProgram, rd: str, rs: str, num: int) -> None:
    """Shift Right Arithmetic.

    :param program:
    :param rd:
    :param rs:
    :param num:
    """
    msb = program.registers[rs] & 0x8000_0000
    program.registers[rd] = program.registers[rs] << num
    program.registers[rd] |= msb


@mips_instruction(PTRN, parse)
def sll(program: MipsProgram, rd: str, rt: str, num: int) -> None:
    """Shift Left Logical.

    :param program:
    :param rt:
    :param rs:
    :param num:
    """
    program.registers[rd] = (program.registers[rt] << num) & 0xFFFF_FFFF


@mips_instruction(PTRN, parse)
def srl(program: MipsProgram, rd: str, rt: str, num: int) -> None:
    """Shift Right Logical.

    :param program:
    :param rt:
    :param rs:
    :param num:
    """
    program.registers[rd] = (program.registers[rt] >> num) & 0xFFFF_FFFF
