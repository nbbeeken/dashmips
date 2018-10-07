"""Two Register Instructions."""
from dashmips.instructions import mips_instruction

PTRN = r"{instr_gap}({register}){args_gap}({register})"


def parse(arg):
    """Two Register Instructions Parser.

    :param arg:

    """
    return (arg[2], arg[3])


@mips_instruction(PTRN, parse)
def jalr(program, rs, rt):
    """Jump and link register.

    :param program:
    :param rt:
    :param rs:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse)
def madd(program, rs, rt):
    """Multiply Add.

    :param program:
    :param rt:
    :param rs:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse)
def maddu(program, rs, rt):
    """Multiply Add Unsigned.

    :param program:
    :param rt:
    :param rs:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse)
def msubu(program, rs, rt):
    """Multiply Subtract Unsigned.

    :param program:
    :param rt:
    :param rs:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse)
def msub(program, rs, rt):
    """Multiply Subtract.

    :param program:
    :param rt:
    :param rs:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse)
def multu(program, rs, rt):
    """Multiply Unsigned.

    :param program:
    :param rt:
    :param rs:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse)
def mult(program, rs, rt):
    """Multiply.

    :param program:
    :param rt:
    :param rs:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse)
def clo(program, rs, rt):
    """Count number of leading ones in Reg[rt].

    :param program:
    :param rt:
    :param rs:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse)
def clz(program, rs, rt):
    """Count number of leading zeros in Reg[rt].

    :param program:
    :param rt:
    :param rs:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse)
def div(program, rs, rt):
    """Divide.

    :param program:
    :param rt:
    :param rs:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse)
def divu(program, rs, rt):
    """Divide unsigned.

    :param program:
    :param rt:
    :param rs:

    """
    raise NotImplementedError('TODO')
