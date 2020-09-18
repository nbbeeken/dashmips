"""Three Register instructions."""
from typing import Tuple
from re import search

from . import mips_instruction
from ..models import MipsProgram

PATTERN = r"{instr_gap}({register}){args_gap}({register}){args_gap}({register})"


def parse(args: Tuple[str, str, str, str, str]) -> Tuple[str, str, str]:
    """Parser for rd rs rt format instructions."""
    return (args[2], args[3], args[4])


@mips_instruction(PATTERN, parse)
def add(program: MipsProgram, rd: str, rs: str, rt: str):
    """Add Reg[rd] = Reg[rs] + Reg[rt]."""
    program.registers[rd] = program.registers[rs] + program.registers[rt]


@mips_instruction(PATTERN, parse)
def addu(program: MipsProgram, rd: str, rs: str, rt: str):
    """Add unsigned Reg[rd] = Reg[rs] + Reg[rt]."""
    program.registers[rd] = program.registers[rs] + program.registers[rt]


@mips_instruction(PATTERN, parse)
def _and(program: MipsProgram, rd: str, rs: str, rt: str):
    """Bitwise And Reg[rd] = Reg[rs] & Reg[rt]."""
    program.registers[rd] = program.registers[rs] & program.registers[rt]


@mips_instruction(PATTERN, parse)
def movn(program: MipsProgram, rd: str, rs: str, rt: str):
    """Move conditional Reg[rd] = Reg[rs] if Reg[rt] != 0."""
    if program.registers[rt] != 0:
        program.registers[rd] = program.registers[rs]


@mips_instruction(PATTERN, parse)
def movz(program: MipsProgram, rd: str, rs: str, rt: str):
    """Move conditional Reg[rd] = Reg[rs] if Reg[rt] == 0."""
    if program.registers[rt] == 0:
        program.registers[rd] = program.registers[rs]


@mips_instruction(PATTERN, parse)
def mul(program: MipsProgram, rd: str, rs: str, rt: str):
    """Multiplication without overflow."""
    # FIXME: Correctness check.
    product = program.registers[rs] * program.registers[rt]
    program.registers["hi"] = product & 0xFFFFFFFF_00000000
    program.registers["lo"] = product & 0x00000000_FFFFFFFF


@mips_instruction(PATTERN, parse)
def nor(program: MipsProgram, rd: str, rs: str, rt: str):
    """Bitwise Nor Reg[rd] = ~(Reg[rs] | Reg[rt])."""
    program.registers[rd] = ~(program.registers[rs] | program.registers[rt])


@mips_instruction(PATTERN, parse)
def _or(program: MipsProgram, rd: str, rs: str, rt: str):
    """Bitwise And Reg[rd] = Reg[rs] | Reg[rt]."""
    program.registers[rd] = program.registers[rs] | program.registers[rt]


@mips_instruction(r"{instr_gap}({register}){args_gap}({register}){args_gap}({register}|{number})", parse)
def rol(program: MipsProgram, rd: str, rs: str, rt: str):
    """Rotate Left Reg[rd] = Reg[rs] << Reg[rt]."""
    bit_shift = program.registers[rt] if search(r"(?:\$(?:(?:0|t[0-9]|s[0-7]|v[0-1]|a[0-3])|zero|sp|fp|gp|ra))", rt) else int(rt)
    program.registers[rd] = (program.registers[rs] << bit_shift) | (program.registers[rs] >> (32 - bit_shift)) & 0xFFFFFFFF


@mips_instruction(r"{instr_gap}({register}){args_gap}({register}){args_gap}({register}|{number})", parse)
def ror(program: MipsProgram, rd: str, rs: str, rt: str):
    """Rotate Right Reg[rd] = Reg[rs] >> Reg[rt]."""
    bit_shift = program.registers[rt] if search(r"(?:\$(?:(?:0|t[0-9]|s[0-7]|v[0-1]|a[0-3])|zero|sp|fp|gp|ra))", rt) else int(rt)
    program.registers[rd] = (program.registers[rs] >> bit_shift) | (program.registers[rs] << (32 - bit_shift)) & 0xFFFFFFFF


@mips_instruction(PATTERN, parse)
def sllv(program: MipsProgram, rd: str, rs: str, rt: str):
    """Shift Left Logical."""
    program.registers[rd] = program.registers[rs] << program.registers[rt]


@mips_instruction(PATTERN, parse)
def slt(program: MipsProgram, rd: str, rs: str, rt: str):
    """Set on less than."""
    if program.registers[rs] < program.registers[rt]:
        program.registers[rd] = 1
    else:
        program.registers[rd] = 0


@mips_instruction(PATTERN, parse)
def sltu(program: MipsProgram, rd: str, rs: str, rt: str):
    """Set on less than unsigned."""
    if abs(program.registers[rs]) < abs(program.registers[rt]):
        program.registers[rd] = 1
    else:
        program.registers[rd] = 0


@mips_instruction(PATTERN, parse)
def srav(program: MipsProgram, rd: str, rs: str, rt: str):
    """Bitwise Shift Right Arithmetic Variable."""
    msb = program.registers[rs] & 0x8000_0000
    program.registers[rd] = program.registers[rs] << program.registers[rt]
    program.registers[rd] |= msb


@mips_instruction(PATTERN, parse)
def srlv(program: MipsProgram, rd: str, rs: str, rt: str):
    """Bitwise Shift Right Logical Variable."""
    program.registers[rd] = program.registers[rs] >> program.registers[rt]


@mips_instruction(PATTERN, parse)
def sub(program: MipsProgram, rd: str, rs: str, rt: str):
    """Subtract Reg[rd] = Reg[rs] - Reg[rt]."""
    program.registers[rd] = program.registers[rs] - program.registers[rt]


@mips_instruction(PATTERN, parse)
def subu(program: MipsProgram, rd: str, rs: str, rt: str):
    """Subtract unsigned Reg[rd] = Reg[rs] - Reg[rt]."""
    program.registers[rd] = program.registers[rs] - program.registers[rt]


@mips_instruction(PATTERN, parse)
def xor(program: MipsProgram, rd: str, rs: str, rt: str):
    """Bitwise And Reg[rd] = Reg[rs] ^ Reg[rt]."""
    program.registers[rd] = program.registers[rs] ^ program.registers[rt]
