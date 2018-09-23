from dashmips.instructions import mips_instruction

PTRN = r"{instr_gap}({register}){args_gap}({register})"


def parse(arg):
    return (arg[2], arg[3])


@mips_instruction(PTRN, parse)
def jalr(program, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def madd(program, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def maddu(program, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def msubu(program, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def msub(program, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def multu(program, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def mult(program, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def clo(program, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def clz(program, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def div(program, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def divu(program, rs, rt):
    raise Exception('TODO: Not Implemented')
