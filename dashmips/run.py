"""MIPS Runner."""
import re

from dashmips.instructions import Instructions
from dashmips.preprocessor import MipsProgram


def run(program: MipsProgram):
    """Execute Preprocessed Mips."""
    program.registers['pc'] = program.labels['main'].value
    while True:
        current_pc = program.registers['pc']
        if len(program.source) < current_pc:
            # We jumped or executed beyond available text
            raise Exception(f'Bad pc value {current_pc}')

        lineofcode = program.source[current_pc].line  # line to execute
        instruction = lineofcode.split(' ')[0]  # Grab the instruction name

        instruction_fn = Instructions[instruction]  # relevant Instruction()

        match = re.match(instruction_fn.regex, lineofcode)
        if match:
            # Instruction has the correct format
            args = instruction_fn.parser(match)
            instruction_fn(program, args)
        else:
            # Bad arguments to instruction
            raise Exception(f"{lineofcode} is malformed for {instruction}")
