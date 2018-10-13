"""MIPS Runner."""
import re

from dashmips.mips import MipsException
from dashmips.instructions import Instructions
from dashmips.preprocessor import MipsProgram


def run(program: MipsProgram, runnable=lambda p: p.registers['pc'] != -1):
    """Execute Preprocessed Mips.

    :param program: MipsProgram:
    :param runnable:  (Default value = lambda p: p.registers['pc'] != -1)

    """
    while runnable(program):
        next_instruction(program)


def next_instruction(program):
    """Execute One Instruction.

    :param program:

    """
    current_pc = program.registers['pc']
    if len(program.source) < current_pc:
        # We jumped or executed beyond available text
        raise MipsException(f'Bad pc value {current_pc}')

    line = program.source[current_pc].line  # line to execute
    instruction = line.split(' ')[0]  # Grab the instruction name

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
