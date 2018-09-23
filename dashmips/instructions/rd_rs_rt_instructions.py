from dashmips.instructions import mips_instruction

PTRN = r"{instr_gap}({register}){args_gap}({register}){args_gap}({register})"


def parser(args):
    """Parser for rd rs rt format instructions."""
    return (args[2], args[3], args[4])


@mips_instruction(PTRN, parser)
def add(program, rd, rs, rt):
    """Add Reg[rd]=Reg[rs]+Reg[rt]."""
    # TODO: @mrunal what's the behavoir??
    program.registers[rd] = ((program.registers[rs] + program.registers[rt]) & 0xFFFF_FFFF)


@mips_instruction(PTRN, parser)
def addu(program, rd, rs, rt):
    """Add unsigned Reg[rd]=Reg[rs]+Reg[rt]."""
    program.registers[rd] = ((program.registers[rs] + program.registers[rt]) & 0xFFFF_FFFF)


@mips_instruction(PTRN, parser)
def _and(program, rd, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parser)
def movn(program, rd, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parser)
def movz(program, rd, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parser)
def mul(program, rd, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parser)
def nor(program, rd, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parser)
def _or(program, rd, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parser)
def sllv(program, rd, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parser)
def slt(program, rd, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parser)
def sltu(program, rd, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parser)
def srav(program, rd, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parser)
def srlv(program, rd, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parser)
def sub(program, rd, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parser)
def subu(program, rd, rs, rt):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parser)
def xor(program, rd, rs, rt):
    raise Exception('TODO: Not Implemented')
