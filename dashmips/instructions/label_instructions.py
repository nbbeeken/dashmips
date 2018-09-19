"""Instructions that accept a label as an argument."""
from dashmips.mips import mips_instruction

PTRN = r"{instr_gap}({label})"


def parse(args):
    """Parse label to pass to instruction function."""
    return (str(args[2]),)


@mips_instruction(PTRN, parse)
def j(regs, lbls, label):
    """Jump unconditionally to label."""
    return None


@mips_instruction(PTRN, parse)
def jal(regs, lbls, label):
    """Jump unconditionally to label and set $ra to current $pc."""
    return None
