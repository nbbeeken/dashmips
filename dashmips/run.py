"""MIPS Runner."""
from typing import List, Dict, Any
import re

import dashmips.mips as mips
import dashmips.hw as hw
from dashmips.instructions import Instructions

from dashmips.preprocessor import Label

from pprint import pprint


def exec_mips(labels: Dict[str, Label], code: List[str], registers, memory):
    """Execute Preprocessed Mips."""
    registers['pc'] = labels['main'].value
    while True:
        current_pc = registers['pc']
        if len(code) < current_pc:
            raise Exception(f'Bad pc value {current_pc}')
        lineofcode = code[current_pc]
        instruction = lineofcode.split(' ')[0]

        instruction_fn = Instructions[instruction]
        match = re.match(instruction_fn.regex, lineofcode)
        if match:
            args = instruction_fn.parser(match)
            instruction_fn(registers, labels, memory, code, args)
        if current_pc == registers['pc']:
            # If a instruction didn't explicitly set the PC
            # FIXME: Edge case: jump to label that is the current_pc
            registers['pc'] += 1
