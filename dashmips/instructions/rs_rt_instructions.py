"""Two Register Instructions."""
from typing import Tuple

from . import mips_instruction
from ..models import MipsProgram

PATTERN = r"{instr_gap}({register}){args_gap}({register})"


def parse(arg: Tuple[str, str, str, str]) -> Tuple[str, str]:
    """Two Register Instructions Parser."""
    return (arg[2], arg[3])


@mips_instruction(PATTERN, parse)
def jalr(program: MipsProgram, rs: str, rt: str):
    """Jump and link register. Store pc into rs, jump to rt."""
    program.registers[rs] = program.registers["pc"]
    program.registers["pc"] = program.registers[rt] - 1


@mips_instruction(PATTERN, parse)
def madd(program: MipsProgram, rs: str, rt: str):
    """Multiply Add."""
    product = program.registers[rs] * program.registers[rt]
    program.registers["hi"] += product & 0xFFFFFFFF_00000000
    program.registers["lo"] += product & 0x00000000_FFFFFFFF


@mips_instruction(PATTERN, parse)
def maddu(program: MipsProgram, rs: str, rt: str):
    """Multiply Add Unsigned."""
    product = abs(program.registers[rs]) * abs(program.registers[rt])
    program.registers["hi"] += product & 0xFFFFFFFF_00000000
    program.registers["lo"] += product & 0x00000000_FFFFFFFF


@mips_instruction(PATTERN, parse)
def msubu(program: MipsProgram, rs: str, rt: str):
    """Multiply Subtract Unsigned."""
    product = abs(program.registers[rs]) * abs(program.registers[rt])
    program.registers["hi"] -= product & 0xFFFFFFFF_00000000
    program.registers["lo"] -= product & 0x00000000_FFFFFFFF


@mips_instruction(PATTERN, parse)
def msub(program: MipsProgram, rs: str, rt: str):
    """Multiply Subtract."""
    product = program.registers[rs] * program.registers[rt]
    program.registers["hi"] -= product & 0xFFFFFFFF_00000000
    program.registers["lo"] -= product & 0x00000000_FFFFFFFF


@mips_instruction(PATTERN, parse)
def multu(program: MipsProgram, rs: str, rt: str):
    """Multiply Unsigned."""
    product = abs(program.registers[rs]) * abs(program.registers[rt])
    program.registers["hi"] = product & 0xFFFFFFFF_00000000
    program.registers["lo"] = product & 0x00000000_FFFFFFFF


@mips_instruction(PATTERN, parse)
def mult(program: MipsProgram, rs: str, rt: str):
    """Multiply."""
    product = program.registers[rs] * program.registers[rt]
    program.registers["hi"] = product & 0xFFFFFFFF_00000000
    program.registers["lo"] = product & 0x00000000_FFFFFFFF


@mips_instruction(PATTERN, parse)
def clo(program: MipsProgram, rs: str, rt: str):
    """Count number of leading ones in Reg[rt]."""
    bit_to_check = 1 << 32
    val = program.registers[rt]
    count = 0
    while (val & bit_to_check) == 1 and bit_to_check > 0:
        count += 1
        bit_to_check >>= 1
    program.registers[rs] = count


@mips_instruction(PATTERN, parse)
def clz(program: MipsProgram, rs: str, rt: str):
    """Count number of leading zeros in Reg[rt]."""
    bit_to_check = 1 << 32
    val = program.registers[rt]
    count = 0
    while (val & bit_to_check) == 0 and bit_to_check > 0:
        count += 1
        bit_to_check >>= 1
    program.registers[rs] = count


@mips_instruction(PATTERN, parse)
def div(program: MipsProgram, rs: str, rt: str):
    """Divide."""
    quotient = program.registers[rs] / program.registers[rt]
    remainder = program.registers[rs] % program.registers[rt]
    program.registers["hi"] = remainder
    program.registers["lo"] = int(quotient)


@mips_instruction(PATTERN, parse)
def divu(program: MipsProgram, rs: str, rt: str):
    """Divide unsigned."""
    quotient = abs(program.registers[rs]) / abs(program.registers[rt])
    remainder = abs(program.registers[rs]) % abs(program.registers[rt])
    program.registers["hi"] = remainder
    program.registers["lo"] = int(quotient)
