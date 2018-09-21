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
    pprint(labels)
    pprint(code)
    print(memory)

    print('\n--- Program Output Start ---\n')

    for instruction in code:

        for instruction_fn in Instructions:
            match = re.match(instruction_fn.regex, instruction)
            if match:
                matches = [match[i] for i in range(0, match.re.groups + 1)]
                args = instruction_fn.parser(match)
                instruction_fn(registers, labels, memory, code, args)
                break
        else:
            print(f'instruction "{instruction}" not recognized')
            exit(1)

    print('\n--- Program Output End ---\n')

    print(registers.pretty_str())
