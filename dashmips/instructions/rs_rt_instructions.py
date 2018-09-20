from dashmips.instructions import mips_instruction

PTRN = r"{instr_gap}({register}){args_gap}({register})"


def parse(arg):
    return (arg[2], arg[3])


@mips_instruction(PTRN, parse)
def jalr(regs, lbls, rs, rt):
    return None


@mips_instruction(PTRN, parse)
def madd(regs, lbls, rs, rt):
    return None


@mips_instruction(PTRN, parse)
def maddu(regs, lbls, rs, rt):
    return None


@mips_instruction(PTRN, parse)
def msubu(regs, lbls, rs, rt):
    return None


@mips_instruction(PTRN, parse)
def msub(regs, lbls, rs, rt):
    return None


@mips_instruction(PTRN, parse)
def multu(regs, lbls, rs, rt):
    return None


@mips_instruction(PTRN, parse)
def mult(regs, lbls, rs, rt):
    return None


@mips_instruction(PTRN, parse)
def clo(regs, lbls, rs, rt):
    return None


@mips_instruction(PTRN, parse)
def clz(regs, lbls, rs, rt):
    return None


@mips_instruction(PTRN, parse)
def div(regs, lbls, rs, rt):
    return None


@mips_instruction(PTRN, parse)
def divu(regs, lbls, rs, rt):
    return None
