"""Instructions that accept a label as an argument."""
from typing import Tuple

from dashmips.instructions import mips_instruction
from dashmips.models import MipsProgram

PTRN = r"{instr_gap}({label})"


def parse(args: Tuple[str, str, str]) -> Tuple[str]:
    """Parse label to pass to instruction function.

    :param args:
    """
    return (args[2],)


@mips_instruction(PTRN, parse, label=True)
def j(program: MipsProgram, address: str) -> None:
    """Jump unconditionally to label.

    :param program:
    :param address:
    """
    program.registers["pc"] = program.labels[address].value


@mips_instruction(PTRN, parse, label=True)
def jal(program: MipsProgram, address: str) -> None:
    """Jump unconditionally to label and set $ra to current $pc.

    :param program:
    :param address:
    """
    program.registers["$ra"] = program.registers["pc"] + 1
    program.registers["pc"] = program.labels[address].value
