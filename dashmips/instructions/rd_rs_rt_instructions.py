"""Three Register instructions."""
from dashmips.instructions import mips_instruction

PTRN = r"{instr_gap}({register}){args_gap}({register}){args_gap}({register})"


def parser(args):
    """Parser for rd rs rt format instructions.

    :param args:

    """
    return (args[2], args[3], args[4])


@mips_instruction(PTRN, parser)
def add(program, rd, rs, rt):
    """Add Reg[rd]=Reg[rs]+Reg[rt].

    :param program:
    :param rs:
    :param rd:
    :param rt:

    """
    # TODO: @mrunal what's the behavoir??
    program.registers[rd] = (
        (program.registers[rs] + program.registers[rt]) & 0xFFFF_FFFF
    )


@mips_instruction(PTRN, parser)
def addu(program, rd, rs, rt):
    """Add unsigned Reg[rd]=Reg[rs]+Reg[rt].

    :param program:
    :param rs:
    :param rd:
    :param rt:

    """
    program.registers[rd] = (
        (program.registers[rs] + program.registers[rt]) & 0xFFFF_FFFF
    )


@mips_instruction(PTRN, parser)
def _and(program, rd, rs, rt):
    """Bitwise And Reg[rd]=Reg[rs]&Reg[rt].

    :param program:
    :param rs:
    :param rd:
    :param rt:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parser)
def movn(program, rd, rs, rt):
    """Move conditional Reg[rd]=Reg[rs] if Reg[rt] != 0.

    :param program:
    :param rs:
    :param rd:
    :param rt:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parser)
def movz(program, rd, rs, rt):
    """Move conditional Reg[rd]=Reg[rs] if Reg[rt] == 0.

    :param program:
    :param rs:
    :param rd:
    :param rt:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parser)
def mul(program, rd, rs, rt):
    """Multiplication without overflow.

    :param program:
    :param rs:
    :param rd:
    :param rt:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parser)
def nor(program, rd, rs, rt):
    """Bitwise Nor Reg[rd]=~(Reg[rs]|Reg[rt]).

    :param program:
    :param rs:
    :param rd:
    :param rt:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parser)
def _or(program, rd, rs, rt):
    """Bitwise And Reg[rd]=Reg[rs]|Reg[rt].

    :param program:
    :param rs:
    :param rd:
    :param rt:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parser)
def sllv(program, rd, rs, rt):
    """Shift Left Logical.

    :param program:
    :param rs:
    :param rd:
    :param rt:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parser)
def slt(program, rd, rs, rt):
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


@mips_instruction(PTRN, parser)
def sltu(program, rd, rs, rt):
    """Set on less than unsigned.

    :param program:
    :param rs:
    :param rd:
    :param rt:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parser)
def srav(program, rd, rs, rt):
    """Bitwise Shift Right Arithmetic Variable.

    :param program:
    :param rs:
    :param rd:
    :param rt:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parser)
def srlv(program, rd, rs, rt):
    """Bitwise Shift Right Logical Variable.

    :param program:
    :param rs:
    :param rd:
    :param rt:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parser)
def sub(program, rd, rs, rt):
    """Subtract Reg[rd]=Reg[rs]-Reg[rt].

    :param program:
    :param rs:
    :param rd:
    :param rt:

    """
    program.registers[rd] = program.registers[rs] - program.registers[rt]


@mips_instruction(PTRN, parser)
def subu(program, rd, rs, rt):
    """Subtract unsigned Reg[rd]=Reg[rs]-Reg[rt].

    :param program:
    :param rs:
    :param rd:
    :param rt:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parser)
def xor(program, rd, rs, rt):
    """Bitwise And Reg[rd]=Reg[rs]^Reg[rt].

    :param program:
    :param rs:
    :param rd:
    :param rt:

    """
    raise NotImplementedError('TODO')
