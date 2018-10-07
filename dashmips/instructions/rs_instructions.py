"""Single Register insructions."""
from dashmips.instructions import mips_instruction

PTRN = r"{instr_gap}({register})"


def parse(arg):
    """Single Register instruction parser.

    :param arg:

    """
    return (arg[2],)


@mips_instruction(PTRN, parse)
def jr(program, rs):
    """Jump to address in Reg[rs].

    :param program:
    :param rs:

    """
    raise NotImplementedError('TODO')
