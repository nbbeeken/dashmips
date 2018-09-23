from dashmips.instructions import mips_instruction

PTRN = r"{instr_gap}({register})"


def parse(args):
    return (args[2],)


@mips_instruction(PTRN, parse)
def mflo(program, rd):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def mfhi(program, rd):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def mthi(program, rd):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def mtlo(program, rd):
    raise Exception('TODO: Not Implemented')
