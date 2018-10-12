"""Register Immediate (Label) instructions."""
from dashmips.instructions import mips_instruction

PTRN = r"{instr_gap}({register}){args_gap}({label})"


def parse(arg):
    """Parser for reg imm insructions.

    :param arg:

    """
    return (arg[2], arg[3])


@mips_instruction(PTRN, parse, label=True)
def bgez(program, rs, label):
    """Branch if Reg[rs] >= 0.

    :param program:
    :param label:
    :param rs:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse, label=True)
def bgezal(program, rs, label):
    """Branch if Reg[rs] >= 0 and link.

    :param program:
    :param label:
    :param rs:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse, label=True)
def bgtz(program, rs, label):
    """Branch if Reg[rs] > 0.

    :param program:
    :param label:
    :param rs:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse, label=True)
def blez(program, rs, label):
    """Branch if Reg[rs] <= 0.

    :param program:
    :param label:
    :param rs:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse, label=True)
def bltz(program, rs, label):
    """Branch if Reg[rs] < 0.

    :param program:
    :param label:
    :param rs:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse, label=True)
def bltzal(program, rs, label):
    """Branch if Reg[rs] < 0 and link.

    :param program:
    :param label:
    :param rs:

    """
    raise NotImplementedError('TODO')
