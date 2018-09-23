"""Instructions that accept a label as an argument."""
from dashmips.instructions import mips_instruction

PTRN = r"{instr_gap}({number})"


def parse(args):
    """Parse label to pass to instruction function."""
    return (int(args[2]),)


@mips_instruction(PTRN, parse)
def j(program, address: int):
    """Jump unconditionally to label."""
    program.registers['pc'] = address


@mips_instruction(PTRN, parse)
def jal(program, address: int):
    """Jump unconditionally to label and set $ra to current $pc."""
    raise Exception('TODO: Not Implemented')
