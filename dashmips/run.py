"""MIPS Runner."""
from typing import List, Dict, Any
import re

from dashmips.MipsProgram import MipsProgram, MipsException

import dashmips.mips as mips
import dashmips.hw as hw
from dashmips.instructions import Instructions

from dashmips.preprocessor import Label

from pprint import pprint


def exec_mips(program: MipsProgram):
    """Execute Preprocessed Mips."""
    program.registers['pc'] = program.labels['main'].value
    while True:
        current_pc = program.registers['pc']
        if len(program.code) < current_pc:
            # We jumped or executed beyond available text
            raise MipsException(f'Bad pc value {current_pc}')

        lineofcode = program.code[current_pc]  # Current line of execution
        instruction = lineofcode.split(' ')[0]  # Grab the instruction name

        instruction_fn = Instructions[instruction]  # relevant Instruction()

        match = re.match(instruction_fn.regex, lineofcode)
        if match:
            # Instruction has the correct format
            args = instruction_fn.parser(match)
            instruction_fn(program, args)
        else:
            # Bad arguments to instruction
            raise MipsException(f"{lineofcode} is malformed for {instruction}")

        if current_pc == program.registers['pc']:
            # If a instruction didn't explicitly set the PC
            # FIXME: Edge case: jump to label that is the current_pc
            program.registers['pc'] += 1  # What?? not pc + 4?? haha.


def debug_mips(labels: Dict[str, Label], code: List[str], registers, memory):
    """Create a debugging instance of mips."""
    pass
