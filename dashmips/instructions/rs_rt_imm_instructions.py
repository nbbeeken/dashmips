"""Two Register and Immediate instructions."""
from dashmips.instructions import mips_instruction, parse_int


PTRN = r"{instr_gap}({register}){args_gap}({register}){args_gap}({number})"


def parse(arg):
    """Two Register and Immediate instructions Parser.

    :param arg:

    """
    return (arg[2], arg[3], parse_int(arg[4]))


@mips_instruction(PTRN, parse)
def addi(program, rs, rt, num):
    """Add immediate Reg[rs]=Reg[rt]+immediate.

    :param program:
    :param rt:
    :param rs:
    :param num:

    """
    program.registers[rs] = program.registers[rt] + num


@mips_instruction(PTRN, parse)
def addiu(program, rs, rt, num):
    """Add immediate unsigned Reg[rs]=Reg[rt]+immediate.

    :param program:
    :param rt:
    :param rs:
    :param num:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse)
def ori(program, rs, rt, num):
    """Or immediate Reg[rs]=Reg[rt]|immediate.

    :param program:
    :param rt:
    :param rs:
    :param num:

    """
    program.registers[rs] = program.registers[rt] | num


@mips_instruction(PTRN, parse)
def andi(program, rs, rt, num):
    """And immediate Reg[rs]=Reg[rt]&immediate.

    :param program:
    :param rt:
    :param rs:
    :param num:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse)
def slti(program, rs, rt, num):
    """Set on less than immediate.

    :param program:
    :param rt:
    :param rs:
    :param num:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse)
def sltiu(program, rs, rt, num):
    """Set on less than immediate unsigned.

    :param program:
    :param rt:
    :param rs:
    :param num:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse)
def xori(program, rs, rt, num):
    """Xor immediate Reg[rs]=Reg[rt]^immediate.

    :param program:
    :param rt:
    :param rs:
    :param num:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse)
def sra(program, rs, rt, num):
    """Shift Right Arithmetic.

    :param program:
    :param rt:
    :param rs:
    :param num:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse)
def sll(program, rd, rt, num):
    """Shift Left Logical.

    :param program:
    :param rt:
    :param rs:
    :param num:

    """
    program.registers[rd] = (program.registers[rt] << num) & 0xFFFF_FFFF


@mips_instruction(PTRN, parse)
def srl(program, rs, rt, num):
    """Shift Right Logical.

    :param program:
    :param rt:
    :param rs:
    :param num:

    """
    raise NotImplementedError('TODO')
