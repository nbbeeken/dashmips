"""Two Register Instructions."""
from typing import Tuple, cast

from dashmips.instructions import mips_instruction
from dashmips.models import MipsProgram

PTRN = r"{instr_gap}({register}){args_gap}({register})"


def parse(arg: Tuple[str, str, str, str]) -> Tuple[str, str]:
    """Two Register Instructions Parser.

    :param arg:
    """
    return (arg[2], arg[3])


@mips_instruction(PTRN, parse)
def jalr(program: MipsProgram, rs: str, rt: str) -> None:
    """Jump and link register. Store pc into rs, jump to rt.

    :param program:
    :param rt:
    :param rs:
    """
    program.registers[rs] = program.registers["pc"]
    program.registers["pc"] = program.registers[rt]


@mips_instruction(PTRN, parse)
def madd(program: MipsProgram, rs: str, rt: str) -> None:
    """Multiply Add.

    :param program:
    :param rt:
    :param rs:
    """
    product = program.registers[rs] * program.registers[rt]
    program.registers["hi"] += product & 0xFFFFFFFF_00000000
    program.registers["lo"] += product & 0x00000000_FFFFFFFF


@mips_instruction(PTRN, parse)
def maddu(program: MipsProgram, rs: str, rt: str) -> None:
    """Multiply Add Unsigned.

    :param program:
    :param rt:
    :param rs:
    """
    product = abs(program.registers[rs]) * abs(program.registers[rt])
    program.registers["hi"] += product & 0xFFFFFFFF_00000000
    program.registers["lo"] += product & 0x00000000_FFFFFFFF


@mips_instruction(PTRN, parse)
def msubu(program: MipsProgram, rs: str, rt: str) -> None:
    """Multiply Subtract Unsigned.

    :param program:
    :param rt:
    :param rs:
    """
    product = abs(program.registers[rs]) * abs(program.registers[rt])
    program.registers["hi"] -= product & 0xFFFFFFFF_00000000
    program.registers["lo"] -= product & 0x00000000_FFFFFFFF


@mips_instruction(PTRN, parse)
def msub(program: MipsProgram, rs: str, rt: str) -> None:
    """Multiply Subtract.

    :param program:
    :param rt:
    :param rs:
    """
    product = program.registers[rs] * program.registers[rt]
    program.registers["hi"] -= product & 0xFFFFFFFF_00000000
    program.registers["lo"] -= product & 0x00000000_FFFFFFFF


@mips_instruction(PTRN, parse)
def multu(program: MipsProgram, rs: str, rt: str) -> None:
    """Multiply Unsigned.

    :param program:
    :param rt:
    :param rs:
    """
    product = abs(program.registers[rs]) * abs(program.registers[rt])
    program.registers["hi"] = product & 0xFFFFFFFF_00000000
    program.registers["lo"] = product & 0x00000000_FFFFFFFF


@mips_instruction(PTRN, parse)
def mult(program: MipsProgram, rs: str, rt: str) -> None:
    """Multiply.

    :param program:
    :param rt:
    :param rs:
    """
    product = program.registers[rs] * program.registers[rt]
    program.registers["hi"] = product & 0xFFFFFFFF_00000000
    program.registers["lo"] = product & 0x00000000_FFFFFFFF


@mips_instruction(PTRN, parse)
def clo(program: MipsProgram, rs: str, rt: str) -> None:
    """Count number of leading ones in Reg[rt].

    :param program:
    :param rt:
    :param rs:
    """
    bit_to_check = 1 << 32
    val = program.registers[rt]
    count = 0
    while (val & bit_to_check) == 1 and bit_to_check > 0:
        count += 1
        bit_to_check >>= 1
    program.registers[rs] = count


@mips_instruction(PTRN, parse)
def clz(program: MipsProgram, rs: str, rt: str) -> None:
    """Count number of leading zeros in Reg[rt].

    :param program:
    :param rt:
    :param rs:
    """
    bit_to_check = 1 << 32
    val = program.registers[rt]
    count = 0
    while (val & bit_to_check) == 0 and bit_to_check > 0:
        count += 1
        bit_to_check >>= 1
    program.registers[rs] = count


@mips_instruction(PTRN, parse)
def div(program: MipsProgram, rs: str, rt: str) -> None:
    """Divide.

    :param program:
    :param rt:
    :param rs:
    """
    quotient = program.registers[rs] / program.registers[rt]
    remainder = program.registers[rs] % program.registers[rt]
    program.registers["hi"] = remainder
    program.registers["lo"] = int(quotient)


@mips_instruction(PTRN, parse)
def divu(program: MipsProgram, rs: str, rt: str) -> None:
    """Divide unsigned.

    :param program:
    :param rt:
    :param rs:
    """
    quotient = abs(program.registers[rs]) / abs(program.registers[rt])
    remainder = abs(program.registers[rs]) % abs(program.registers[rt])
    program.registers["hi"] = remainder
    program.registers["lo"] = int(quotient)
