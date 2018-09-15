"""Instructions that accept a label as an argument."""
from mips import Instruction

PTRN = r"{instr_gap}({label})"


def parse(args):
    """Parse label to pass to instruction function."""
    return (str(args[2]),)


@Instruction(PTRN, parse)
def j(regs, lbls, label):
    """Jump unconditionally to label."""
    return None


@Instruction(PTRN, parse)
def jal(regs, lbls, label):
    """Jump unconditionally to label and set $ra to current $pc."""
    return None
