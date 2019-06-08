"""MIPS Runner."""
import re
import sys

from typing import Callable

from dashmips.instructions import Instructions
from dashmips.mips import MipsException
from dashmips.models import MipsProgram

RUN_COND: Callable[[MipsProgram], bool] = (lambda p: p.registers["pc"] != -1)


def run(
    program: MipsProgram, runnable: Callable[[MipsProgram], bool] = RUN_COND
) -> int:
    """Execute Preprocessed Mips.

    :param program: MipsProgram:
    :param runnable:  (Default value = lambda p: p.registers['pc'] != -1)
    """
    try:
        while runnable(program):
            next_instruction(program)
    except MipsException as mips_ex:
        print(f"{mips_ex.message} on ", file=sys.stderr, end="")
        print(
            f"{program.current_line.filename}:{program.current_line.lineno}",
            file=sys.stderr,
        )
        sys.exit()

    return program.registers["$a0"]  # should hold program exit code


def next_instruction(program: MipsProgram) -> None:
    """Execute One Instruction.

    :param program:
    """
    current_pc = program.registers["pc"]
    if len(program.source) < current_pc:
        # We jumped or executed beyond available text
        raise MipsException(f"Bad pc value {current_pc}")

    line = program.source[current_pc].line  # line to execute
    instruction = line.split(" ")[0]  # Grab the instruction name

    instruction_fn = Instructions[instruction]  # relevant Instruction()

    match = re.match(instruction_fn.regex, line)
    if match:
        # Instruction has the correct format
        args = instruction_fn.parser(match)
        instruction_fn(program, args)
    else:
        # Bad arguments to instruction
        lineno = program.source[current_pc].lineno
        raise MipsException(f"'{line}':{lineno} malformed for '{instruction}'")
