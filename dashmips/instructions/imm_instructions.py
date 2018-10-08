"""Instructions that accept a label as an argument."""
from dashmips.instructions import mips_instruction, parse_int

PTRN = r"{instr_gap}({number})"


def parse(args):
    """Parse label to pass to instruction function.

    :param args:

    """
    return (parse_int(args[2]),)


@mips_instruction(PTRN, parse, label=True)
def j(program, address: int):
    """Jump unconditionally to label.

    :param program:
    :param address: int:

    """
    program.registers['pc'] = address


@mips_instruction(PTRN, parse, label=True)
def jal(program, address: int):
    """Jump unconditionally to label and set $ra to current $pc.

    :param program:
    :param address: int:

    """
    raise NotImplementedError('TODO')
