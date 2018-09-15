from mips import Instruction

PTRN = r"{instr_gap}({register}){args_gap}({register}){args_gap}({register})"


def parser(args):
    return (args[2], args[3], args[4])


@Instruction(PTRN, parser)
def add(regs, lbls, rd, rs, rt):
    return None


@Instruction(PTRN, parser)
def addu(regs, lbls, rd, rs, rt):
    return None


@Instruction(PTRN, parser)
def _and(regs, lbls, rd, rs, rt):
    return None


@Instruction(PTRN, parser)
def movn(regs, lbls, rd, rs, rt):
    return None


@Instruction(PTRN, parser)
def movz(regs, lbls, rd, rs, rt):
    return None


@Instruction(PTRN, parser)
def mul(regs, lbls, rd, rs, rt):
    return None


@Instruction(PTRN, parser)
def nor(regs, lbls, rd, rs, rt):
    return None


@Instruction(PTRN, parser)
def _or(regs, lbls, rd, rs, rt):
    return None


@Instruction(PTRN, parser)
def sllv(regs, lbls, rd, rs, rt):
    return None


@Instruction(PTRN, parser)
def slt(regs, lbls, rd, rs, rt):
    return None


@Instruction(PTRN, parser)
def sltu(regs, lbls, rd, rs, rt):
    return None


@Instruction(PTRN, parser)
def srav(regs, lbls, rd, rs, rt):
    return None


@Instruction(PTRN, parser)
def srlv(regs, lbls, rd, rs, rt):
    return None


@Instruction(PTRN, parser)
def sub(regs, lbls, rd, rs, rt):
    return None


@Instruction(PTRN, parser)
def subu(regs, lbls, rd, rs, rt):
    return None


@Instruction(PTRN, parser)
def xor(regs, lbls, rd, rs, rt):
    return None
