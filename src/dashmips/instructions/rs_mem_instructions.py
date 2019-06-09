"""Register and Memory access Instructions."""
from typing import Tuple, cast

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
    """Load Byte from memory.

    :param program:
    :param num:
    :param rs:
    :param rt:
    """
    program.registers[rs] = program.memory[num + program.registers[rt]]


@mips_instruction(PTRN, parse)
def lbu(program: MipsProgram, rs: str, num: int, rt: str) -> None:
    """Load Byte Unsigned from memory.

    :param program:
    :param num:
    :param rs:
    :param rt:
    """
    program.registers[rs] = abs(program.memory[num + program.registers[rt]])


@mips_instruction(PTRN, parse)
def lh(program: MipsProgram, rs: str, num: int, rt: str) -> None:
    """Load half-word from memory.

    :param program:
    :param num:
    :param rs:
    :param rt:
    """
    # FIXME: This does not sign extend correctly
    addr = num + program.registers[rt]
    val = 0
    vals = program.memory[addr: addr + 2]
    for i, b in enumerate(reversed(vals)):
        val |= b << i * 8
    program.registers[rs] = val


@mips_instruction(PTRN, parse)
def lhu(program: MipsProgram, rs: str, num: int, rt: str) -> None:
    """Load half-word unsigned from memory.

    :param program:
    :param num:
    :param rs:
    :param rt:
    """
    addr = num + program.registers[rt]
    val = 0
    vals = program.memory[addr: addr + 2]
    for i, b in enumerate(reversed(vals)):
        val |= b << i * 8
    program.registers[rs] = val


@mips_instruction(PTRN, parse)
def lw(program: MipsProgram, rs: str, num: int, rt: str) -> None:
    """Load word from memory.

    :param program:
    :param num:
    :param rs:
    :param rt:
    """
    addr = num + program.registers[rt]
    val = 0
    vals = program.memory[addr: addr + 4]
    for i, b in enumerate(reversed(vals)):
        val |= b << i * 8
    program.registers[rs] = val


@mips_instruction(PTRN, parse)
def sb(program: MipsProgram, rs: str, num: int, rt: str) -> None:
    """Store Byte to memory.

    :param program:
    :param num:
    :param rs:
    :param rt:
    """
    val = program.registers[rs]
    program.memory[num + program.registers[rt]] = val & 0xFF


@mips_instruction(PTRN, parse)
def sw(program: MipsProgram, rs: str, num: int, rt: str) -> None:
    """Store word to memory.

    :param program:
    :param num:
    :param rs:
    :param rt:
    """
    val = program.registers[rs]
    addr = num + program.registers[rt]
    program.memory[addr: addr + 4] = val.to_bytes(4, "big")


@mips_instruction(PTRN, parse)
def sh(program: MipsProgram, rs: str, num: int, rt: str) -> None:
    """Store halfword to memory.

    :param program:
    :param num:
    :param rs:
    :param rt:
    """
    val = program.registers[rs]
    addr = num + program.registers[rt]
    program.memory[addr: addr + 2] = val.to_bytes(2, "big")
