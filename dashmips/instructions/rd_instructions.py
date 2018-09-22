from dashmips.instructions import mips_instruction

PTRN = r"{instr_gap}({register})"


def parse(args):
    return (args[2],)


@mips_instruction(PTRN, parse)
def mflo(registers, labels, memory, code, rd):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def mfhi(registers, labels, memory, code, rd):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def mthi(registers, labels, memory, code, rd):
    raise Exception('TODO: Not Implemented')


@mips_instruction(PTRN, parse)
def mtlo(registers, labels, memory, code, rd):
    raise Exception('TODO: Not Implemented')
