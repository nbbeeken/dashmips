"""Three Register instructions."""
from typing import Tuple, cast

from dashmips.instructions import mips_instruction
from dashmips.models import MipsProgram

PTRN = r"{instr_gap}({register}){args_gap}({register}){args_gap}({register})"


def parse(args: Tuple[str, str, str, str, str]) -> Tuple[str, str, str]:
    """Parser for rd rs rt format instructions.

    :param args:
    """
    return (args[2], args[3], args[4])


@mips_instruction(PTRN, parse)
def add(program: MipsProgram, rd: str, rs: str, rt: str) -> None:
    """Add Reg[rd] = Reg[rs] + Reg[rt].

    :param program:
    :param rs:
    :param rd:
    :param rt:
    """
    program.registers[rd] = program.registers[rs] + program.registers[rt]


@mips_instruction(PTRN, parse)
def addu(program: MipsProgram, rd: str, rs: str, rt: str) -> None:
    """Add unsigned Reg[rd] = Reg[rs] + Reg[rt].

    :param program:
    :param rs:
    :param rd:
    :param rt:
    """
    program.registers[rd] = program.registers[rs] + program.registers[rt]


@mips_instruction(PTRN, parse)
def _and(program: MipsProgram, rd: str, rs: str, rt: str) -> None:
    """Bitwise And Reg[rd] = Reg[rs] & Reg[rt].

    :param program:
    :param rs:
    :param rd:
    :param rt:
    """
    program.registers[rd] = program.registers[rs] & program.registers[rt]


@mips_instruction(PTRN, parse)
def movn(program: MipsProgram, rd: str, rs: str, rt: str) -> None:
    """Move conditional Reg[rd] = Reg[rs] if Reg[rt] != 0.

    :param program:
    :param rs:
    :param rd:
    :param rt:
    """
    if program.registers[rt] != 0:
        program.registers[rd] = program.registers[rs]


@mips_instruction(PTRN, parse)
def movz(program: MipsProgram, rd: str, rs: str, rt: str) -> None:
    """Move conditional Reg[rd] = Reg[rs] if Reg[rt] == 0.

    :param program:
    :param rs:
    :param rd:
    :param rt:
    """
    if program.registers[rt] == 0:
        program.registers[rd] = program.registers[rs]


@mips_instruction(PTRN, parse)
def mul(program: MipsProgram, rd: str, rs: str, rt: str) -> None:
    """Multiplication without overflow.

    :param program:
    :param rs:
    :param rd:
    :param rt:
    """
    # FIXME: Correctness check.
    product = program.registers[rs] * program.registers[rt]
    program.registers["hi"] = product & 0xFFFFFFFF_00000000
    program.registers["lo"] = product & 0x00000000_FFFFFFFF


@mips_instruction(PTRN, parse)
def nor(program: MipsProgram, rd: str, rs: str, rt: str) -> None:
    """Bitwise Nor Reg[rd] = ~(Reg[rs] | Reg[rt]).

    :param program:
    :param rs:
    :param rd:
    :param rt:
    """
    program.registers[rd] = ~(program.registers[rs] | program.registers[rt])


@mips_instruction(PTRN, parse)
def _or(program: MipsProgram, rd: str, rs: str, rt: str) -> None:
    """Bitwise And Reg[rd] = Reg[rs] | Reg[rt].

    :param program:
    :param rs:
    :param rd:
    :param rt:
    """
    program.registers[rd] = program.registers[rs] | program.registers[rt]


@mips_instruction(PTRN, parse)
def sllv(program: MipsProgram, rd: str, rs: str, rt: str) -> None:
    """Shift Left Logical.

    :param program:
    :param rs:
    :param rd:
    :param rt:
    """
    program.registers[rd] = program.registers[rs] << program.registers[rt]


@mips_instruction(PTRN, parse)
def slt(program: MipsProgram, rd: str, rs: str, rt: str) -> None:
    """Set on less than.

    :param program:
    :param rs:
    :param rd:
    :param rt:
    """
    if program.registers[rs] < program.registers[rt]:
        program.registers[rd] = 1
    else:
        program.registers[rd] = 0


@mips_instruction(PTRN, parse)
def sltu(program: MipsProgram, rd: str, rs: str, rt: str) -> None:
    """Set on less than unsigned.

    :param program:
    :param rs:
    :param rd:
    :param rt:
    """
    if abs(program.registers[rs]) < abs(program.registers[rt]):
        program.registers[rd] = 1
    else:
        program.registers[rd] = 0


@mips_instruction(PTRN, parse)
def srav(program: MipsProgram, rd: str, rs: str, rt: str) -> None:
    """Bitwise Shift Right Arithmetic Variable.

    :param program:
    :param rs:
    :param rd:
    :param rt:
    """
    msb = program.registers[rs] & 0x8000_0000
    program.registers[rd] = program.registers[rs] << program.registers[rt]
    program.registers[rd] |= msb


@mips_instruction(PTRN, parse)
def srlv(program: MipsProgram, rd: str, rs: str, rt: str) -> None:
    """Bitwise Shift Right Logical Variable.

    :param program:
    :param rs:
    :param rd:
    :param rt:
    """
    program.registers[rd] = program.registers[rs] >> program.registers[rt]


@mips_instruction(PTRN, parse)
def sub(program: MipsProgram, rd: str, rs: str, rt: str) -> None:
    """Subtract Reg[rd] = Reg[rs] - Reg[rt].

    :param program:
    :param rs:
    :param rd:
    :param rt:
    """
    program.registers[rd] = program.registers[rs] - program.registers[rt]


@mips_instruction(PTRN, parse)
def subu(program: MipsProgram, rd: str, rs: str, rt: str) -> None:
    """Subtract unsigned Reg[rd] = Reg[rs] - Reg[rt].

    :param program:
    :param rs:
    :param rd:
    :param rt:
    """
    program.registers[rd] = program.registers[rs] - program.registers[rt]


@mips_instruction(PTRN, parse)
def xor(program: MipsProgram, rd: str, rs: str, rt: str) -> None:
    """Bitwise And Reg[rd] = Reg[rs] ^ Reg[rt].

    :param program:
    :param rs:
    :param rd:
    :param rt:
    """
    program.registers[rd] = program.registers[rs] ^ program.registers[rt]
