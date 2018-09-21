from dashmips.instructions import mips_instruction

PTRN = r"{instr_gap}({register}){args_gap}({number}?)\(({register})\)"


def parse(arg):
    return (arg[2], int(arg[3]), arg[4])


@mips_instruction(PTRN, parse)
def lb(registers, labels, memory, code, rs, num, rt):
    return None


@mips_instruction(PTRN, parse)
def lbu(registers, labels, memory, code, rs, num, rt):
    return None


@mips_instruction(PTRN, parse)
def lh(registers, labels, memory, code, rs, num, rt):
    return None


@mips_instruction(PTRN, parse)
def lhu(registers, labels, memory, code, rs, num, rt):
    return None


@mips_instruction(PTRN, parse)
def lw(registers, labels, memory, code, rs, num, rt):
    return None


@mips_instruction(PTRN, parse)
def lwl(registers, labels, memory, code, rs, num, rt):
    return None


@mips_instruction(PTRN, parse)
def sc(registers, labels, memory, code, rs, num, rt):
    return None


@mips_instruction(PTRN, parse)
def lwr(registers, labels, memory, code, rs, num, rt):
    return None


@mips_instruction(PTRN, parse)
def sb(registers, labels, memory, code, rs, num, rt):
    return None


@mips_instruction(PTRN, parse)
def sw(registers, labels, memory, code, rs, num, rt):
    return None


@mips_instruction(PTRN, parse)
def swl(registers, labels, memory, code, rs, num, rt):
    return None


@mips_instruction(PTRN, parse)
def swr(registers, labels, memory, code, rs, num, rt):
    return None


@mips_instruction(PTRN, parse)
def sh(registers, labels, memory, code, rs, num, rt):
    return None
