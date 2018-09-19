from dashmips.mips import Instruction

PTRN = r"{instr_gap}({register})"


def parse(args):
    return (args[2],)


@Instruction(PTRN, parse)
def mflo(regs, lbls, rd):
    return None


@Instruction(PTRN, parse)
def mfhi(regs, lbls, rd):
    return None


@Instruction(PTRN, parse)
def mthi(regs, lbls, rd):
    return None


@Instruction(PTRN, parse)
def mtlo(regs, lbls, rd):
    return None
