from dashmips.instructions import mips_instruction

PTRN = r"{instr_gap}({register})"


def parse(args):
    return (args[2],)


@mips_instruction(PTRN, parse)
def mflo(regs, lbls, rd):
    return None


@mips_instruction(PTRN, parse)
def mfhi(regs, lbls, rd):
    return None


@mips_instruction(PTRN, parse)
def mthi(regs, lbls, rd):
    return None


@mips_instruction(PTRN, parse)
def mtlo(regs, lbls, rd):
    return None
