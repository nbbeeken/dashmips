from dashmips.mips import Instruction

PTRN = r"{instr_gap}({register}){args_gap}({number}?)\(({register})\)"


def parse(arg):
    return (arg[2],  int(arg[3]), arg[4])


@Instruction(PTRN, parse)
def lb(regs, lbls, rs, num, rt):
    return None


@Instruction(PTRN, parse)
def lbu(regs, lbls, rs, num, rt):
    return None


@Instruction(PTRN, parse)
def lh(regs, lbls, rs, num, rt):
    return None


@Instruction(PTRN, parse)
def lhu(regs, lbls, rs, num, rt):
    return None


@Instruction(PTRN, parse)
def lw(regs, lbls, rs, num, rt):
    return None


@Instruction(PTRN, parse)
def lwl(regs, lbls, rs, num, rt):
    return None


@Instruction(PTRN, parse)
def sc(regs, lbls, rs, num, rt):
    return None


@Instruction(PTRN, parse)
def lwr(regs, lbls, rs, num, rt):
    return None


@Instruction(PTRN, parse)
def sb(regs, lbls, rs, num, rt):
    return None


@Instruction(PTRN, parse)
def sw(regs, lbls, rs, num, rt):
    return None


@Instruction(PTRN, parse)
def swl(regs, lbls, rs, num, rt):
    return None


@Instruction(PTRN, parse)
def swr(regs, lbls, rs, num, rt):
    return None


@Instruction(PTRN, parse)
def sh(regs, lbls, rs, num, rt):
    return None
