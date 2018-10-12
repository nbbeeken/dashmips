"""Instuctions that operate on one register."""
from dashmips.instructions import mips_instruction

PTRN = r"{instr_gap}({register}){args_gap}({register}){args_gap}({label})"


def parse(arg):
    """Two Register and Immediate instructions Parser.

    :param arg:

    """
    return (arg[2], arg[3], arg[4])


@mips_instruction(PTRN, parse)
def beq(program, rs, rt, label):
    """Branch to label if Reg[rs] == Reg[rt].

    :param program:
    :param rt:
    :param rs:
    :param label:

    """
    if program.registers[rs] == program.registers[rt]:
        program.registers['pc'] = program.labels[label].value


@mips_instruction(PTRN, parse)
def bne(program, rs, rt, label):
    """Branch to label if Reg[rs] != Reg[rt].

    :param program:
    :param rt:
    :param rs:
    :param label:

    """
    if program.registers[rs] != program.registers[rt]:
        program.registers['pc'] = program.labels[label].value
