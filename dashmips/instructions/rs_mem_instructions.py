from dashmips.instructions import mips_instruction

PTRN = r"{instr_gap}({register}){args_gap}({number}?)\(({register})\)"


def parse(arg):
    return (arg[2], int(arg[3]), arg[4])


@mips_instruction(PTRN, parse)
def lb(program, rs, num, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def lbu(program, rs, num, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def lh(program, rs, num, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def lhu(program, rs, num, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def lw(program, rs, num, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def lwl(program, rs, num, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def sc(program, rs, num, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def lwr(program, rs, num, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def sb(program, rs, num, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def sw(program, rs, num, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def swl(program, rs, num, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def swr(program, rs, num, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def sh(program, rs, num, rt):
    raise Exception('TODO: Not Implemented')
