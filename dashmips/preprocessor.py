"""Preprocessor for mips assembly."""
from typing import List, Dict, Any, Tuple
import re
import dashmips.mips as mips
import dashmips.hw as hw
from dataclasses import dataclass


@dataclass
class Label:
    """Multiprupose human name for data/address."""

    type: str
    value: int
    name: str

    text = 'text'
    data = 'data'


def preprocess(code: str, memory) -> Tuple[Dict[str, Label], List[str]]:
    """
    Prepare Mips for running.

    Breaks the code into directive and text sections.
    """
    # Clean out comments and empty lines
    linesofcode = [
        re.sub(mips.RE.COMMENT, '', line).strip()
        for line in [
            line
            for line in code.splitlines() if line
        ]
    ]

    labels: Dict[str, Label] = {}

    unprocessed_labels, unprocessed_code = split_to_sections(linesofcode)

    data_labels(labels, unprocessed_labels, memory)
    processed_code = code_labels(labels, unprocessed_code)

    return labels, processed_code


def split_to_sections(code) -> Tuple[List[str], List[str]]:
    """
    Handle file with mixed sections.

    .text and .data sections can come in any order.
    """
    if code[0] in [mips.RE.DATA_SEC, mips.RE.TEXT_SEC]:
        section = code[0]
    else:
        section = None

    if not section:
        raise Exception("first line must be .text/.data")

    sections: Dict[str, Any] = {mips.RE.DATA_SEC: [], mips.RE.TEXT_SEC: []}
    for line in code:
        if line not in [mips.RE.DATA_SEC, mips.RE.TEXT_SEC]:
            sections[section].append(line)
        else:
            section = line
    return sections[mips.RE.DATA_SEC], sections[mips.RE.TEXT_SEC]


def data_labels(labels: Dict[str, Label], data_sec: List[str], memory):
    """
    Construct the .data section to spec.

    Fill the .data section memory with user defined static data
    """
    data_line_re = f"({mips.RE.LABEL}):\\s*({mips.RE.DIRECTIVE})\\s+(.*)"
    for line in data_sec:
        match = re.match(data_line_re, line)
        if match:
            name = match[1]
            directive = mips.Directives[match[2][1:]]
            address = directive(name, match[3], memory)
            labels[name] = Label(name=name, value=address, type=Label.data)


def code_labels(labels: Dict[str, Label], text_sec: List[str]) -> List[str]:
    """
    Construct the .text section to spec.

    Fill the .text section memory with user code
    """
    text = []
    lbl_ct = 0
    for idx, line in enumerate(text_sec):
        # For each line in the stipped text section, check for label
        match = re.match(f"({mips.RE.LABEL}):", line)
        if match:
            # If there's a label save it to the labels dictionary
            labels[match[1]] = Label(type=Label.text,
                                     value=(idx - lbl_ct), name=match[1])
            if len(line) > len(match[0]):
                # If the line is longer than what was matched, lets assume
                # the rest is an instruction (comments and whitespace should
                # already have been stripped) we cut out the label
                text.append(line[len(match[0]):].strip())
            else:
                # To offset the previously removed label lines
                lbl_ct += 1
        else:
            # Otherwise save the line as is
            text.append(line)

    # Converting in code labels to values
    for idx, line in enumerate(text):
        for name, label in labels.items():
            # For each label modify the string so that the
            # label is replaced with the value
            if name in line:
                text[idx] = line.replace(name, str(label.value))

    return text
