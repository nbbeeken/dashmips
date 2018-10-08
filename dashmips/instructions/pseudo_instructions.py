"""Instructions that are not real."""
from dashmips.instructions import mips_instruction, parse_int

PTRN = r"{instr_gap}({register}){args_gap}({number})"


@mips_instruction(PTRN, lambda args: (args[2], int(args[3])), label=True)
def la(program, rd, address):
    """Load address.

    :param program:
    :param address:
    :param rd:

    """
    program.registers[rd] = address


@mips_instruction(PTRN, lambda args: (args[2], parse_int(args[3])))
def li(program, rd, number):
    """Load immediate.

    :param program:
    :param number:
    :param rd:

    """
    program.registers[rd] = number


@mips_instruction(
    r"{instr_gap}({register}){args_gap}({register})",
    lambda args: (args[2], args[3])
)
def move(program, rd, rs):
    """Overwrite rd with rs.

    :param program:
    :param rs:
    :param rd:

    """
    program.registers[rd] = program.registers[rs]
