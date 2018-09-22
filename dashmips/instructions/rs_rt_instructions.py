from dashmips.instructions import mips_instruction

PTRN = r"{instr_gap}({register}){args_gap}({register})"


def parse(arg):
    return (arg[2], arg[3])


@mips_instruction(PTRN, parse)
def jalr(registers, labels, memory, code, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def madd(registers, labels, memory, code, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def maddu(registers, labels, memory, code, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def msubu(registers, labels, memory, code, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def msub(registers, labels, memory, code, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def multu(registers, labels, memory, code, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def mult(registers, labels, memory, code, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def clo(registers, labels, memory, code, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def clz(registers, labels, memory, code, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def div(registers, labels, memory, code, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def divu(registers, labels, memory, code, rs, rt):
    raise Exception('TODO: Not Implemented')
