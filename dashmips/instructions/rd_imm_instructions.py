from dashmips.mips import Instruction

PTRN = r"{instr_gap}({register}){args_gap}({number})"


def parse(args):
    return (args[2], int(args[3]))


@Instruction(PTRN, parse)
def lui():
    return None
