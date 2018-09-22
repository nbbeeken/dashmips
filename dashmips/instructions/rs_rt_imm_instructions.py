from dashmips.instructions import mips_instruction


PTRN = r"{instr_gap}({register}){args_gap}({register}){args_gap}({number})"


def parse(arg):
    return (arg[2], arg[3], int(arg[4]))


@mips_instruction(PTRN, parse)
def addi(registers, labels, memory, code, rs, rt, num):
    registers[rs] = registers[rt] + num


@mips_instruction(PTRN, parse)
def addiu(registers, labels, memory, code, rs, rt, num):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def ori(registers, labels, memory, code, rs, rt, num):
    registers[rs] = registers[rt] | num


@mips_instruction(PTRN, parse)
def andi(registers, labels, memory, code, rs, rt, num):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def slti(registers, labels, memory, code, rs, rt, num):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def sltiu(registers, labels, memory, code, rs, rt, num):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def xori(registers, labels, memory, code, rs, rt, num):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def sra(registers, labels, memory, code, rs, rt, num):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def sll(registers, labels, memory, code, rs, rt, num):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def srl(registers, labels, memory, code, rs, rt, num):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def beq(registers, labels, memory, code, rs, rt, address):
    """Branch to address if Reg[rs] equals Reg[rt]."""
    if registers[rs] == registers[rt]:
        registers['pc'] = address


@mips_instruction(PTRN, parse)
def bne(registers, labels, memory, code, rs, rt, address):
    raise Exception('TODO: Not Implemented')
