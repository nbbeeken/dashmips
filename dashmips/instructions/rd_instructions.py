"""Instuctions that operate on one register."""
from dashmips.instructions import mips_instruction

PTRN = r"{instr_gap}({register})"


def parse(args):
    """Parser for single register instructions.

    :param args:

    """
    return (args[2],)


@mips_instruction(PTRN, parse)
def mflo(program, rd):
    """Move from lo register to Reg[rd].

    :param program:
    :param rd:

    """
    program.registers[rd] = program.registers['lo']


@mips_instruction(PTRN, parse)
def mfhi(program, rd):
    """Move from hi register to Reg[rd].

    :param program:
    :param rd:

    """
    program.registers[rd] = program.registers['hi']


@mips_instruction(PTRN, parse)
def mthi(program, rd):
    """Move to hi register from Reg[rd].

    :param program:
    :param rd:

    """
    program.registers['hi'] = program.registers[rd]


@mips_instruction(PTRN, parse)
def mtlo(program, rd):
    """Move to lo register from Reg[rd].

    :param program:
    :param rd:

    """
    program.registers['lo'] = program.registers[rd]
