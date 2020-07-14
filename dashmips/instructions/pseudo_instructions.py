"""Instructions that are not real."""
from . import mips_instruction
from ..models import MipsProgram
from ..utils import parse_int


@mips_instruction(r"{instr_gap}({register}){args_gap}({label})", lambda args: (args[2], args[3]), label=True)
def la(program: MipsProgram, rd: str, address: str):
    """Load address from immediate."""
    program.registers[rd] = program.labels[address].value


@mips_instruction(r"{instr_gap}({register}){args_gap}({number})", lambda args: (args[2], parse_int(args[3])))
def li(program: MipsProgram, rd: str, number: int):
    """Load immediate."""
    program.registers[rd] = number


@mips_instruction(r"{instr_gap}({register}){args_gap}({register})", lambda args: (args[2], args[3]))
def move(program: MipsProgram, rd: str, rs: str):
    """Overwrite rd with rs."""
    program.registers[rd] = program.registers[rs]


@mips_instruction(r"{instr_gap}({register}){args_gap}({label})", lambda args: (args[2], args[3]))
def beqz(program: MipsProgram, rd: str, label: str):
    """Branch to label if Reg[rd] == 0."""
    if program.registers[rd] == 0:
        program.registers["pc"] = program.labels[label].value - 1


@mips_instruction(r"{instr_gap}({register}){args_gap}({label})", lambda args: (args[2], args[3]))
def bnez(program: MipsProgram, rd: str, label: str):
    """Branch to label if Reg[rd] != 0."""
    if program.registers[rd] != 0:
        program.registers["pc"] = program.labels[label].value - 1


@mips_instruction(r"{instr_gap}({label})", lambda args: (args[2],))
def b(program: MipsProgram, label: str):
    """Branch unconditionally to label."""
    program.registers["pc"] = program.labels[label].value - 1


@mips_instruction(
    r"{instr_gap}({register}){args_gap}({register}|{number}){args_gap}({label})", lambda args: (args[2], args[3], args[4]),
)
def bgt(program: MipsProgram, rd: str, rs: str, label: str):
    """Branch to label if Reg[rd]>Reg[rs]."""
    if rs not in program.registers:
        rs_val = parse_int(rs)
    else:
        rs_val = program.registers[rs]

    if program.registers[rd] > rs_val:
        program.registers["pc"] = program.labels[label].value - 1


@mips_instruction(r"{instr_gap}({register}){args_gap}({register}|{number}){args_gap}({label})", lambda args: (args[2], args[3], args[4]))
def blt(program: MipsProgram, rd: str, rs: str, label: str):
    """Branch to label if Reg[rd]<Reg[rs]."""
    if rs not in program.registers:
        rs_val = parse_int(rs)
    else:
        rs_val = program.registers[rs]

    if program.registers[rd] < rs_val:
        program.registers["pc"] = program.labels[label].value - 1


@mips_instruction(r"{instr_gap}({register}){args_gap}({register})", lambda args: (args[2], args[3]))
def neg(program: MipsProgram, rd: str, rs: str):
    """Negate Reg[rs] and store in Reg[rd]."""
    program.registers[rd] = ((~program.registers[rs]) & 0xFFFF_FFFF) + 1


@mips_instruction(
    r"{instr_gap}({register}){args_gap}({register}){args_gap}({label})", lambda args: (args[2], args[3], args[4]),
)
def bge(program: MipsProgram, rd: str, rs: str, label: str):
    """Branch to label if Reg[rd]>Reg[rs]."""
    if program.registers[rd] > program.registers[rs]:
        program.registers["pc"] = program.labels[label].value - 1


@mips_instruction(
    r"{instr_gap}({register}){args_gap}({register}){args_gap}({label})", lambda args: (args[2], args[3], args[4]),
)
def ble(program: MipsProgram, rd: str, rs: str, label: str):
    """Branch to label if Reg[rd]<Reg[rs]."""
    if program.registers[rd] < program.registers[rs]:
        program.registers["pc"] = program.labels[label].value - 1
