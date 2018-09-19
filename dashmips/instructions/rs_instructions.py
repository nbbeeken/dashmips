from dashmips.mips import Instruction

PTRN = r"{instr_gap}({register})"


def parse(arg):
    return (arg[2],)


@Instruction(PTRN, parse)
def jr(regs, lbls, rs):
    return None
