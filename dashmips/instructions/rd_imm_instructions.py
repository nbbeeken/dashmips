"""Instructions that accept a register and immediate as an argument."""
from dashmips.mips import Instruction

PTRN = r"{instr_gap}({register}){args_gap}({number})"


def parse(args):
    """Parse rd and imm to pass to instruction function."""
    return (args[2], int(args[3]))


@Instruction(PTRN, parse)
def lui():
    """Load upper immediate."""
    return None
