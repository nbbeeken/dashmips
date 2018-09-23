from dashmips.instructions import mips_instruction

PTRN = r"{instr_gap}({register})"


def parse(arg):
    return (arg[2],)


@mips_instruction(PTRN, parse)
def jr(program, rs):
    raise Exception('TODO: Not Implemented')
