"""Register and Memory access Instructions."""
from dashmips.instructions import mips_instruction, parse_int

PTRN = r"{instr_gap}({register}){args_gap}({number}?)\(({register})\)"


def parse(args):
    """Register and Memory access Instructions Parser.

    :param arg:

    """
    offset = 0
    if args[3]:
        offset = parse_int(args[3])

    return (args[2], offset, args[5])


@mips_instruction(PTRN, parse)
def lb(program, rs, num, rt):
    """Load Byte.

    :param program:
    :param num:
    :param rs:
    :param rt:

    """
    program.registers[rs] = program.memory[num + program.registers[rt]]


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
    addr = num + program.registers[rt]
    program.registers[rs] = (
        program.memory[addr + 0] << 0 &
        program.memory[addr + 1] << 8 &
        program.memory[addr + 2] << 16 &
        program.memory[addr + 3] << 24
    )


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
    val = program.registers[rs]
    program.memory[num + program.registers[rt]] = [
        val & 0xFF_00_00_00,
        val & 0x00_FF_00_00,
        val & 0x00_00_FF_00,
        val & 0x00_00_00_FF,
    ]


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
