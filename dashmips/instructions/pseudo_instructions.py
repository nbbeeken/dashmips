"""Instructions that are not real."""
from dashmips.instructions import mips_instruction, parse_int


@mips_instruction(
    r"{instr_gap}({register}){args_gap}({label})",
    lambda args: (args[2], args[3]),
    label=True
)
def la(program, rd, address):
    """Load address.

    :param program:
    :param address:
    :param rd:

    """
    program.registers[rd] = program.labels[address].value


@mips_instruction(
    r"{instr_gap}({register}){args_gap}({number})",
    lambda args: (args[2], parse_int(args[3]))
)
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


@mips_instruction(
    r"{instr_gap}({register}){args_gap}({label})",
    lambda args: (args[2], args[3])
)
def beqz(program, rd, label: str):
    """Branch to label if Reg[rd]==0.

    :param program:
    :param rd:
    :param label:

    """
    if program.registers[rd] == 0:
        program.registers['pc'] = program.labels[label].value


@mips_instruction(
    r"{instr_gap}({register}){args_gap}({label})",
    lambda args: (args[2], args[3])
)
def bnez(program, rd, label: str):
    """Branch to label if Reg[rd]!=0.

    :param program:
    :param rd:
    :param label:

    """
    if program.registers[rd] != 0:
        program.registers['pc'] = program.labels[label].value


@mips_instruction(
    r"{instr_gap}({label})",
    lambda args: (args[2],)
)
def b(program, label: int):
    """Branch.

    :param program:
    :param label:

    """
    program.registers['pc'] = program.labels[label].value


@mips_instruction(
    r"{instr_gap}({register}){args_gap}" +
    r"({register}|{number}){args_gap}({label})",
    lambda args: (args[2], args[3], args[4])
)
def bgt(program, rd, rs, label: str):
    """Branch to label if Reg[rd]>Reg[rs].

    :param program:
    :param label:

    """
    if rs not in program.registers:
        rs_val = parse_int(rs)
    else:
        rs_val = program.registers[rs]

    if program.registers[rd] > rs_val:
        program.registers['pc'] = program.labels[label].value


@mips_instruction(
    r"{instr_gap}({register}){args_gap}" +
    r"({register}|{number}){args_gap}({label})",
    lambda args: (args[2], args[3], args[4])
)
def blt(program, rd, rs, label: int):
    """Branch to label if Reg[rd]<Reg[rs].

    :param program:
    :param label:

    """
    if rs not in program.registers:
        rs_val = parse_int(rs)
    else:
        rs_val = program.registers[rs]

    if program.registers[rd] < rs_val:
        program.registers['pc'] = program.labels[label].value


@mips_instruction(
    r"{instr_gap}({register}){args_gap}({register})",
    lambda args: (args[2], args[3])
)
def neg(program, rd, rs):
    """Negate Reg[rs] and store in Reg[rd].

    :param program:
    :param label:

    """
    program.registers[rd] = ~program.registers[rs]


@mips_instruction(
    r"{instr_gap}({register}){args_gap}({register}){args_gap}({label})",
    lambda args: (args[2], args[3], args[4])
)
def bge(program, rd, rs, label):
    """Branch to label if Reg[rd]>Reg[rs].

    :param program:
    :param label:

    """
    if program.registers[rd] > program.registers[rs]:
        program.registers['pc'] = program.labels[label].value
