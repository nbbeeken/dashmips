"""Instructions that accept a register and immediate as an argument."""
from dashmips.instructions import mips_instruction, parse_int

PTRN = r"{instr_gap}({register}){args_gap}({number})"


def parse(args):
    """Parse rd and imm to pass to instruction function.

    :param args:

    """
    return (args[2], parse_int(args[3]))


@mips_instruction(PTRN, parse)
def lui(program, rd, immediate):
    """Load upper immediate, NOT LOAD FROM MEMORY.

    :param program:
    :param rd:
    :param immediate:

    """
    program.registers[rd] = (immediate << 16) & 0xFFFF_0000
