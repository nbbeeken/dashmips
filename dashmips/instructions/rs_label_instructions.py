from dashmips.instructions import mips_instruction

PTRN = r"{instr_gap}({register}){args_gap}({label})"


def parse(arg):
    return (arg[2], str(arg[3]))


@mips_instruction(PTRN, parse)
def bgez(regs, lbls, rs, label):
    return None


@mips_instruction(PTRN, parse)
def bgezal(regs, lbls, rs, label):
    return None


@mips_instruction(PTRN, parse)
def bgtz(regs, lbls, rs, label):
    return None


@mips_instruction(PTRN, parse)
def blez(regs, lbls, rs, label):
    return None


@mips_instruction(PTRN, parse)
def bltz(regs, lbls, rs, label):
    return None


@mips_instruction(PTRN, parse)
def bltzal(regs, lbls, rs, label):
    return None
