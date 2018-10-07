"""Register and Memory access Instructions."""
from dashmips.instructions import mips_instruction, parse_int

PTRN = r"{instr_gap}({register}){args_gap}({number}?)\(({register})\)"


def parse(arg):
    """Register and Memory access Instructions Parser.

    :param arg:

    """
    offset = 0
    if args[3]:
        offset = parse_int(arg[3])

    return (arg[2], offset, arg[4])


@mips_instruction(PTRN, parse)
def lb(program, rs, num, rt):
    """Load Byte.

    :param program:
    :param num:
    :param rs:
    :param rt:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse)
def lbu(program, rs, num, rt):
    """Load Byte Unsigned.

    :param program:
    :param num:
    :param rs:
    :param rt:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse)
def lh(program, rs, num, rt):
    """Load half-word.

    :param program:
    :param num:
    :param rs:
    :param rt:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse)
def lhu(program, rs, num, rt):
    """Load half-word unsigned.

    :param program:
    :param num:
    :param rs:
    :param rt:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse)
def lw(program, rs, num, rt):
    """Load word.

    :param program:
    :param num:
    :param rs:
    :param rt:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse)
def lwl(program, rs, num, rt):
    """Load Word Left: Load from 1 to 4 bytes left-justified into $t1.

    :param program:
    :param num:
    :param rs:
    :param rt:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse)
def lwr(program, rs, num, rt):
    """Load Word Right: Load from 1 to 4 bytes right-justified into $t1.

    :param program:
    :param num:
    :param rs:
    :param rt:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse)
def sb(program, rs, num, rt):
    """Store Byte.

    :param program:
    :param num:
    :param rs:
    :param rt:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse)
def sw(program, rs, num, rt):
    """Store word.

    :param program:
    :param num:
    :param rs:
    :param rt:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse)
def swl(program, rs, num, rt):
    """Store Word Left: Load from 1 to 4 bytes left-justified into $t1.

    :param program:
    :param num:
    :param rs:
    :param rt:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse)
def swr(program, rs, num, rt):
    """Store Word Right: Load from 1 to 4 bytes right-justified into $t1.

    :param program:
    :param num:
    :param rs:
    :param rt:

    """
    raise NotImplementedError('TODO')


@mips_instruction(PTRN, parse)
def sh(program, rs, num, rt):
    """Store halfword.

    :param program:
    :param num:
    :param rs:
    :param rt:

    """
    raise NotImplementedError('TODO')
