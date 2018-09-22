"""Instructions that accept a label as an argument."""
from dashmips.instructions import mips_instruction

PTRN = r"{instr_gap}({number})"


def parse(args):
    """Parse label to pass to instruction function."""
    return (int(args[2]),)


@mips_instruction(PTRN, parse)
def j(registers, labels, memory, code, address: int):
    """Jump unconditionally to label."""
    registers['pc'] = address


@mips_instruction(PTRN, parse)
def jal(registers, labels, memory, code, address: int):
    """Jump unconditionally to label and set $ra to current $pc."""
    raise Exception('TODO: Not Implemented')
