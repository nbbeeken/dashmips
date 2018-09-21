from dashmips.instructions import mips_instruction

PTRN = r"{instr_gap}({register}){args_gap}({number})"


def parse(arg):
    return (arg[2], str(arg[3]))


@mips_instruction(PTRN, parse)
def bgez(registers, labels, memory, code, rs, label):
    return None


@mips_instruction(PTRN, parse)
def bgezal(registers, labels, memory, code, rs, label):
    return None


@mips_instruction(PTRN, parse)
def bgtz(registers, labels, memory, code, rs, label):
    return None


@mips_instruction(PTRN, parse)
def blez(registers, labels, memory, code, rs, label):
    return None


@mips_instruction(PTRN, parse)
def bltz(registers, labels, memory, code, rs, label):
    return None


@mips_instruction(PTRN, parse)
def bltzal(registers, labels, memory, code, rs, label):
    return None
