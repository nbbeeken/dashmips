"""Instructions that are not real."""
from dashmips.instructions import mips_instruction

PTRN = r"{instr_gap}({register}){args_gap}({number})"


@mips_instruction(PTRN, lambda args: (args[2], int(args[3])))
def la(program, rd, address):
    """Load address."""
    program.registers[rd] = address


@mips_instruction(PTRN, lambda args: (args[2], int(args[3])))
def li(program, rd, number):
    """Load address."""
    program.registers[rd] = number


@mips_instruction(
    r"{instr_gap}({register}){args_gap}({register})",
    lambda args: (args[2], args[3])
)
def move(program, rd, rs):
    """Overwrite rd with rs."""
    program.registers[rd] = program.registers[rs]
