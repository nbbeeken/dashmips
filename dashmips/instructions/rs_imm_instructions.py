from dashmips.instructions import mips_instruction

PTRN = r"{instr_gap}({register}){args_gap}({number})"


def parse(arg):
    return (arg[2], str(arg[3]))


@mips_instruction(PTRN, parse)
def bgez(program, rs, label):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def bgezal(program, rs, label):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def bgtz(program, rs, label):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def blez(program, rs, label):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def bltz(program, rs, label):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def bltzal(program, rs, label):
    raise Exception('TODO: Not Implemented')
