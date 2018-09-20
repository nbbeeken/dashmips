from dashmips.instructions import mips_instruction


PTRN = r"{instr_gap}({register}){args_gap}({register}){args_gap}({number})"


def parse(arg):
    return (arg[2], arg[3], int(arg[4]))


@mips_instruction(PTRN, parse)
def addi(regs, lbls, rs, rt, num):
    return regs.update({rs: regs[rt] + num})


@mips_instruction(PTRN, parse)
def addiu(regs, lbls, rs, rt, num):
    return None


@mips_instruction(PTRN, parse)
def ori(regs, lbls, rs, rt, num):
    return None


@mips_instruction(PTRN, parse)
def andi(regs, lbls, rs, rt, num):
    return None


@mips_instruction(PTRN, parse)
def slti(regs, lbls, rs, rt, num):
    return None


@mips_instruction(PTRN, parse)
def sltiu(regs, lbls, rs, rt, num):
    return None


@mips_instruction(PTRN, parse)
def xori(regs, lbls, rs, rt, num):
    return None


@mips_instruction(PTRN, parse)
def sra(regs, lbls, rs, rt, num):
    return None


@mips_instruction(PTRN, parse)
def sll(regs, lbls, rs, rt, num):
    return None


@mips_instruction(PTRN, parse)
def srl(regs, lbls, rs, rt, num):
    return None
