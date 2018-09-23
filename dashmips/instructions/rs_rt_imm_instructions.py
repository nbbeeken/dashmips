from dashmips.instructions import mips_instruction


PTRN = r"{instr_gap}({register}){args_gap}({register}){args_gap}({number})"


def parse(arg):
    return (arg[2], arg[3], int(arg[4]))


@mips_instruction(PTRN, parse)
def addi(program, rs, rt, num):
    program.registers[rs] = program.registers[rt] + num


@mips_instruction(PTRN, parse)
def addiu(program, rs, rt, num):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def ori(program, rs, rt, num):
    program.registers[rs] = program.registers[rt] | num


@mips_instruction(PTRN, parse)
def andi(program, rs, rt, num):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def slti(program, rs, rt, num):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def sltiu(program, rs, rt, num):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def xori(program, rs, rt, num):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def sra(program, rs, rt, num):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def sll(program, rs, rt, num):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def srl(program, rs, rt, num):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def beq(program, rs, rt, address):
    """Branch to address if Reg[rs] equals Reg[rt]."""
    if program.registers[rs] == program.registers[rt]:
        program.registers['pc'] = address


@mips_instruction(PTRN, parse)
def bne(program, rs, rt, address):
    raise Exception('TODO: Not Implemented')
