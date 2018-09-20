from dashmips.instructions import mips_instruction

PTRN = r"{instr_gap}({register}){args_gap}({register}){args_gap}({label})"


def parse(arg):
    return(arg[2], arg[3], str(arg[4]))


@mips_instruction(PTRN, parse)
def beq(regs, lbls, rs, rt, label):
    return None


@mips_instruction(PTRN, parse)
def bne(regs, lbls, rs, rt, label):
    return None
