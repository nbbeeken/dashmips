"""Register Label instructions."""
from dashmips.instructions import mips_instruction

PTRN = r"{instr_gap}({register}){args_gap}({number})"


def parse(arg):
    """Parser for reg imm insructions.

    :param arg:

    """
    return (arg[2], str(arg[3]))


@mips_instruction(PTRN, parse)
def bgez(program, rs, label):
    """Branch if Reg[rs] >= 0.

    :param program:
    :param label:
    :param rs:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse)
def bgezal(program, rs, label):
    """Branch if Reg[rs] >= 0 and link.

    :param program:
    :param label:
    :param rs:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse)
def bgtz(program, rs, label):
    """Branch if Reg[rs] > 0.

    :param program:
    :param label:
    :param rs:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse)
def blez(program, rs, label):
    """Branch if Reg[rs] <= 0.

    :param program:
    :param label:
    :param rs:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse)
def bltz(program, rs, label):
    """Branch if Reg[rs] < 0.

    :param program:
    :param label:
    :param rs:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse)
def bltzal(program, rs, label):
    """Branch if Reg[rs] < 0 and link.

    :param program:
    :param label:
    :param rs:

    """
    raise NotImplementedError('TODO')
