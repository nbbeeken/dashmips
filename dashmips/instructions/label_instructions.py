from dashmips.mips import Instruction

PTRN = r"{instr_gap}({label})"


def parse(args):
    return (str(args[2]),)


@Instruction(PTRN, parse)
def j(regs, lbls, label):
    return None


@Instruction(PTRN, parse)
def jal(regs, lbls, label):
    return None
