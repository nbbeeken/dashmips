"""MIPS Parser."""
from typing import List, Dict, Any
import re
import dashmips.mips as mips
import dashmips.hw as hw

from dashmips.instructions import Instructions

from pprint import pprint as pretty

DATA_SEC = ".data"
TEXT_SEC = ".text"


def preprocess_mips(labels, code) -> dict:
    """
    Prepare Mips for running.

    Breaks the code into directive and text sections.
    """
    code = [line for line in code.splitlines() if line]
    code = [re.sub(mips.RE.COMMENT, '', line).strip() for line in code]

    processed_code = split_to_sections(code)

    for idx, line in enumerate(processed_code[TEXT_SEC]):
        match = re.match(f"({mips.RE.LABEL}):", line)
        if match:
            labels[match[1]] = idx
            del processed_code[TEXT_SEC][idx]

    return processed_code


def split_to_sections(code) -> Dict[str, List[str]]:
    """
    Handle file with mixed sections.

    .text and .data sections can come in any order.
    """
    section = code[0] if code[0] in [DATA_SEC, TEXT_SEC] else None
    if not section:
        raise Exception("first line must be .text/.data")

    sections: Dict[str, List[str]] = {DATA_SEC: [], TEXT_SEC: []}
    for line in code:
        if line not in [DATA_SEC, TEXT_SEC]:
            sections[section].append(line)
        else:
            section = line
    return sections


def build_data(labels: dict, data_sec: list) -> Dict[str, Any]:
    """
    Construct the .data section to spec.

    Fill the .data section memory with user defined static data
    """
    labels = {**labels}
    data_line_re = f"({mips.RE.LABEL}):\\s*({mips.RE.DIRECTIVE})\\s+(.*)"

    for line in data_sec:
        match = re.match(data_line_re, line)
        if match:
            label = match[1]
            direc = match[2][1:]
            datas = match[3]
            labels[label] = mips.MipsDirectives[direc](datas)

    return labels


def exec_mips(code: str):
    """
    Execute Mips.

    code - multiline string of mips (first line MUST be .data/.text)
    """
    labels: dict = {}
    registers = hw.MIPSRegisters()
    memory = hw.MIPSMemory()

    parsedcode = preprocess_mips(labels, code)

    labels = build_data(labels, parsedcode[DATA_SEC])

    for instruction in parsedcode[TEXT_SEC]:

        for instruction_fn in Instructions:
            match = re.match(instruction_fn.regex, instruction)
            if match:
                matches = [match[i] for i in range(0, match.re.groups + 1)]
                args = instruction_fn.parser(match)
                instruction_fn(registers, labels, *args)
                break

    print(registers.pretty_str())
