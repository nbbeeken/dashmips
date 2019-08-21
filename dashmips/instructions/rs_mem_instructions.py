"""Register and Memory access Instructions."""
from typing import Tuple

from . import mips_instruction
from ..models import MipsProgram
from ..utils import parse_int, intify, bytesify

PATTERN = r"{instr_gap}({register}){args_gap}({number}?)\(({register})\)"


def parse(args: Tuple[str, str, str, str, str]) -> Tuple[str, int, str]:
    """Register and Memory access Instructions Parser."""
    offset = 0
    if args[3]:
        offset = parse_int(args[3])

    return (args[2], offset, args[4])


@mips_instruction(PATTERN, parse)
def lb(program: MipsProgram, rs: str, num: int, rt: str):
    """Load Byte from memory."""
    program.registers[rs] = intify(program.memory.read08(num + program.registers[rt]))


@mips_instruction(PATTERN, parse)
def lbu(program: MipsProgram, rs: str, num: int, rt: str):
    """Load Byte Unsigned from memory."""
    program.registers[rs] = intify(program.memory.read08(num + program.registers[rt]), unsigned=True)


@mips_instruction(PATTERN, parse)
def lh(program: MipsProgram, rs: str, num: int, rt: str):
    """Load half-word from memory."""
    # FIXME: This does not sign extend correctly
    address = num + program.registers[rt]
    val = 0
    values = intify(program.memory.read16(address))
    program.registers[rs] = val


@mips_instruction(PATTERN, parse)
def lhu(program: MipsProgram, rs: str, num: int, rt: str):
    """Load half-word unsigned from memory."""
    address = num + program.registers[rt]
    val = 0
    values = program.memory.read16(address)
    program.registers[rs] = intify(values, unsigned=True)


@mips_instruction(PATTERN, parse)
def lw(program: MipsProgram, rs: str, num: int, rt: str):
    """Load word from memory."""
    address = num + program.registers[rt]
    val = 0
    values = program.memory.read32(address)
    program.registers[rs] = intify(values)


@mips_instruction(PATTERN, parse)
def sb(program: MipsProgram, rs: str, num: int, rt: str):
    """Store Byte to memory."""
    value = program.registers[rs]
    address = num + program.registers[rt]
    program.memory.write08(address, bytesify(value, size=1))


@mips_instruction(PATTERN, parse)
def sh(program: MipsProgram, rs: str, num: int, rt: str):
    """Store halfword to memory."""
    value = program.registers[rs]
    address = num + program.registers[rt]
    program.memory.write16(address, bytesify(value, size=2))


@mips_instruction(PATTERN, parse)
def sw(program: MipsProgram, rs: str, num: int, rt: str):
    """Store word to memory."""
    value = program.registers[rs]
    address = num + program.registers[rt]
    program.memory.write32(address, bytesify(value, size=4))
