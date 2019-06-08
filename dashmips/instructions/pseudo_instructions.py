"""Instructions that are not real."""
from dashmips.instructions import mips_instruction, parse_int
from dashmips.models import MipsProgram


@mips_instruction(
    r"{instr_gap}({register}){args_gap}({label})",
    lambda args: (args[2], args[3]),
    label=True,
)
def la(program: MipsProgram, rd: str, address: str) -> None:
    """Load address from immediate.

    :param program:
    :param address:
    :param rd:
    """
    program.registers[rd] = program.labels[address].value


@mips_instruction(
    r"{instr_gap}({register}){args_gap}({number})",
    lambda args: (args[2], parse_int(args[3])),
)
def li(program: MipsProgram, rd: str, number: int) -> None:
    """Load immediate.

    :param program:
    :param number:
    :param rd:
    """
    program.registers[rd] = number


@mips_instruction(
    r"{instr_gap}({register}){args_gap}({register})",
    lambda args: (
        args[2],
        args[3]))
def move(program: MipsProgram, rd: str, rs: str) -> None:
    """Overwrite rd with rs.

    :param program:
    :param rs:
    :param rd:
    """
    program.registers[rd] = program.registers[rs]


@mips_instruction(
    r"{instr_gap}({register}){args_gap}({label})",
    lambda args: (
        args[2],
        args[3]))
def beqz(program: MipsProgram, rd: str, label: str) -> None:
    """Branch to label if Reg[rd] == 0.

    :param program:
    :param rd:
    :param label:
    """
    if program.registers[rd] == 0:
        program.registers["pc"] = program.labels[label].value


@mips_instruction(
    r"{instr_gap}({register}){args_gap}({label})",
    lambda args: (
        args[2],
        args[3]))
def bnez(program: MipsProgram, rd: str, label: str) -> None:
    """Branch to label if Reg[rd] != 0.

    :param program:
    :param rd:
    :param label:
    """
    if program.registers[rd] != 0:
        program.registers["pc"] = program.labels[label].value


@mips_instruction(r"{instr_gap}({label})", lambda args: (args[2],))
def b(program: MipsProgram, label: str) -> None:
    """Branch.

    :param program:
    :param label:
    """
    program.registers["pc"] = program.labels[label].value


@mips_instruction(
    r"{instr_gap}({register}){args_gap}" +
    r"({register}|{number}){args_gap}({label})",
    lambda args: (
        args[2],
        args[3],
        args[4]),
)
def bgt(program: MipsProgram, rd: str, rs: str, label: str) -> None:
    """Branch to label if Reg[rd]>Reg[rs].

    :param program:
    :param label:
    """
    if rs not in program.registers:
        rs_val = parse_int(rs)
    else:
        rs_val = program.registers[rs]

    if program.registers[rd] > rs_val:
        program.registers["pc"] = program.labels[label].value


@mips_instruction(
    r"{instr_gap}({register}){args_gap}" +
    r"({register}|{number}){args_gap}({label})",
    lambda args: (
        args[2],
        args[3],
        args[4]),
)
def blt(program: MipsProgram, rd: str, rs: str, label: str) -> None:
    """Branch to label if Reg[rd]<Reg[rs].

    :param program:
    :param label:
    """
    if rs not in program.registers:
        rs_val = parse_int(rs)
    else:
        rs_val = program.registers[rs]

    if program.registers[rd] < rs_val:
        program.registers["pc"] = program.labels[label].value


@mips_instruction(
    r"{instr_gap}({register}){args_gap}({register})",
    lambda args: (
        args[2],
        args[3]))
def neg(program: MipsProgram, rd: str, rs: str) -> None:
    """Negate Reg[rs] and store in Reg[rd].

    :param program:
    :param label:
    """
    program.registers[rd] = ~program.registers[rs]


@mips_instruction(
    r"{instr_gap}({register}){args_gap}({register}){args_gap}({label})",
    lambda args: (args[2], args[3], args[4]),
)
def bge(program: MipsProgram, rd: str, rs: str, label: str) -> None:
    """Branch to label if Reg[rd]>Reg[rs].

    :param program:
    :param label:
    """
    if program.registers[rd] > program.registers[rs]:
        program.registers["pc"] = program.labels[label].value


@mips_instruction(
    r"{instr_gap}({register}){args_gap}({register}){args_gap}({label})",
    lambda args: (args[2], args[3], args[4]),
)
def ble(program: MipsProgram, rd: str, rs: str, label: str) -> None:
    """Branch to label if Reg[rd]<Reg[rs].

    :param program:
    :param label:
    """
    if program.registers[rd] < program.registers[rs]:
        program.registers["pc"] = program.labels[label].value
