"""Register and Memory access Instructions."""
from typing import Tuple

from dashmips.instructions import mips_instruction, parse_int
from dashmips.models import MipsProgram


PTRN = r"{instr_gap}({register}){args_gap}({number}?)\(({register})\)"


def parse(args: Tuple[str, str, str, str, str]) -> Tuple[str, int, str]:
    """Register and Memory access Instructions Parser.

    :param arg:

    """
    offset = 0
    if args[3]:
        offset = parse_int(args[3])

    return (args[2], offset, args[4])


@mips_instruction(PTRN, parse)
def lb(program: MipsProgram, rs: str, num: int, rt: str) -> None:
    """Load Byte.

    :param program:
    :param num:
    :param rs:
    :param rt:
    """
    program.registers[rs] = program.memory[num + program.registers[rt]]


@mips_instruction(PTRN, parse)
def lbu(program: MipsProgram, rs: str, num: int, rt: str) -> None:
    """Load Byte Unsigned.

    :param program:
    :param num:
    :param rs:
    :param rt:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse)
def lh(program: MipsProgram, rs: str, num: int, rt: str) -> None:
    """Load half-word.

    :param program:
    :param num:
    :param rs:
    :param rt:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse)
def lhu(program: MipsProgram, rs: str, num: int, rt: str) -> None:
    """Load half-word unsigned.

    :param program:
    :param num:
    :param rs:
    :param rt:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse)
def lw(program: MipsProgram, rs: str, num: int, rt: str) -> None:
    """Load word.

    :param program:
    :param num:
    :param rs:
    :param rt:

    """
    addr = num + program.registers[rt]
    val = 0
    vals = program.memory[addr:addr + 4]
    for i, b in enumerate(reversed(vals)):
        val |= b << i * 8
    program.registers[rs] = val


@mips_instruction(PTRN, parse)
def lwl(program: MipsProgram, rs: str, num: int, rt: str) -> None:
    """Load Word Left: Load from 1 to 4 bytes left-justified into $t1.

    :param program:
    :param num:
    :param rs:
    :param rt:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse)
def lwr(program: MipsProgram, rs: str, num: int, rt: str) -> None:
    """Load Word Right: Load from 1 to 4 bytes right-justified into $t1.

    :param program:
    :param num:
    :param rs:
    :param rt:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse)
def sb(program: MipsProgram, rs: str, num: int, rt: str) -> None:
    """Store Byte.

    :param program:
    :param num:
    :param rs:
    :param rt:

    """
    val = program.registers[rs]
    program.memory[num + program.registers[rt]] = val & 0xFF


@mips_instruction(PTRN, parse)
def sw(program: MipsProgram, rs: str, num: int, rt: str) -> None:
    """Store word.

    :param program:
    :param num:
    :param rs:
    :param rt:

    """
    val = program.registers[rs]
    addr = num + program.registers[rt]
    program.memory[addr:addr + 4] = val.to_bytes(4, 'big')


@mips_instruction(PTRN, parse)
def swl(program: MipsProgram, rs: str, num: int, rt: str) -> None:
    """Store Word Left: Load from 1 to 4 bytes left-justified into $t1.

    :param program:
    :param num:
    :param rs:
    :param rt:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse)
def swr(program: MipsProgram, rs: str, num: int, rt: str) -> None:
    """Store Word Right: Load from 1 to 4 bytes right-justified into $t1.

    :param program:
    :param num:
    :param rs:
    :param rt:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse)
def sh(program: MipsProgram, rs: str, num: int, rt: str) -> None:
    """Store halfword.

    :param program:
    :param num:
    :param rs:
    :param rt:

    """
    val = program.registers[rs]
    addr = num + program.registers[rt]
    program.memory[addr:addr + 2] = val.to_bytes(2, 'big')
