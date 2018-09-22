from dashmips.instructions import mips_instruction

PTRN = r"{instr_gap}({register}){args_gap}({register}){args_gap}({register})"


def parser(args):
    """Parser for rd rs rt format instructions."""
    return (args[2], args[3], args[4])


@mips_instruction(PTRN, parser)
def add(registers, labels, memory, code, rd, rs, rt):
    """Add Reg[rd]=Reg[rs]+Reg[rt]."""
    # TODO: @mrunal what's the behavoir??
    registers[rd] = ((registers[rs] + registers[rt]) & 0xFFFF_FFFF)


@mips_instruction(PTRN, parser)
def addu(registers, labels, memory, code, rd, rs, rt):
    """Add unsigned Reg[rd]=Reg[rs]+Reg[rt]."""
    registers[rd] = ((registers[rs] + registers[rt]) & 0xFFFF_FFFF)


@mips_instruction(PTRN, parser)
def _and(registers, labels, memory, code, rd, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parser)
def movn(registers, labels, memory, code, rd, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parser)
def movz(registers, labels, memory, code, rd, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parser)
def mul(registers, labels, memory, code, rd, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parser)
def nor(registers, labels, memory, code, rd, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parser)
def _or(registers, labels, memory, code, rd, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parser)
def sllv(registers, labels, memory, code, rd, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parser)
def slt(registers, labels, memory, code, rd, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parser)
def sltu(registers, labels, memory, code, rd, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parser)
def srav(registers, labels, memory, code, rd, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parser)
def srlv(registers, labels, memory, code, rd, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parser)
def sub(registers, labels, memory, code, rd, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parser)
def subu(registers, labels, memory, code, rd, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parser)
def xor(registers, labels, memory, code, rd, rs, rt):
    raise Exception('TODO: Not Implemented')
