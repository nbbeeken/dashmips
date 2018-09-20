from dashmips.instructions import mips_instruction

PTRN = r"{instr_gap}({register}){args_gap}({number}?)\(({register})\)"


def parse(arg):
    return (arg[2], int(arg[3]), arg[4])


@mips_instruction(PTRN, parse)
def lb(regs, lbls, rs, num, rt):
    return None


@mips_instruction(PTRN, parse)
def lbu(regs, lbls, rs, num, rt):
    return None


@mips_instruction(PTRN, parse)
def lh(regs, lbls, rs, num, rt):
    return None


@mips_instruction(PTRN, parse)
def lhu(regs, lbls, rs, num, rt):
    return None


@mips_instruction(PTRN, parse)
def lw(regs, lbls, rs, num, rt):
    return None


@mips_instruction(PTRN, parse)
def lwl(regs, lbls, rs, num, rt):
    return None


@mips_instruction(PTRN, parse)
def sc(regs, lbls, rs, num, rt):
    return None


@mips_instruction(PTRN, parse)
def lwr(regs, lbls, rs, num, rt):
    return None


@mips_instruction(PTRN, parse)
def sb(regs, lbls, rs, num, rt):
    return None


@mips_instruction(PTRN, parse)
def sw(regs, lbls, rs, num, rt):
    return None


@mips_instruction(PTRN, parse)
def swl(regs, lbls, rs, num, rt):
    return None


@mips_instruction(PTRN, parse)
def swr(regs, lbls, rs, num, rt):
    return None


@mips_instruction(PTRN, parse)
def sh(regs, lbls, rs, num, rt):
    return None
