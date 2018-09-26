"""Preprocessor for mips assembly."""
from typing import List, Dict, Any, Tuple, Optional
import re
import dashmips.mips as mips
import dashmips.hw as hw
from dataclasses import dataclass


@dataclass
class Label:
    """Mips Preprocessor Label."""

    type: str
    value: int
    name: str


lbldict = Dict[str, Label]


def preprocess(code: str, memory) -> Tuple[lbldict, List[str], Dict[int, int]]:
    """
    Prepare Mips for running.

    Breaks the code into directive and text sections.
    """
    linenumbers = list(enumerate(code.splitlines()))
    # remove comments
    nocomments = map(
        lambda ln: (ln[0] + 1, re.sub(mips.RE.COMMENT, '', ln[1]).strip()),
        linenumbers
    )
    # drop lines that are empty
    noemptylines = filter(
        lambda ln: ln[1] != '',
        nocomments
    )
    # make every white space just one space
    linesofcode: List[Tuple[int, str]] = list(map(
        lambda ln: (ln[0], ' '.join(ln[1].split())),
        noemptylines
    ))

    labels: lbldict = {}

    # Gather .data/.text sections into seperate lists
    unprocessed_labels, unprocessed_code = split_to_sections(linesofcode)

    # First process all the .data labels so they can be replaced in .text
    data_labels(labels, unprocessed_labels, memory)
    # Second gather the code labels,
    # this also replaces all labels in code with the correct value
    processed_code = code_labels(labels, unprocessed_code)

    nl_to_ol = {
        nl: ol[0]
        for nl, ol in enumerate(processed_code)
    }

    return labels, [line[1] for line in processed_code], nl_to_ol


sectionsType = Tuple[List[str], List[Tuple[int, str]]]


def split_to_sections(code: List[Tuple[int, str]]) -> sectionsType:
    """
    Handle file with mixed sections.

    .text and .data sections can come in any order.
    """
    section: Optional[str] = None
    if code[0][1] in [mips.RE.DATA_SEC, mips.RE.TEXT_SEC]:
        section = code[0][1]

    if section is None:
        raise Exception("first line must be .text/.data")

    sections: Dict[str, Any] = {mips.RE.DATA_SEC: [], mips.RE.TEXT_SEC: []}
    for lineno, line in code:
        if line not in [mips.RE.DATA_SEC, mips.RE.TEXT_SEC]:
            if section == mips.RE.DATA_SEC:
                sections[section].append(line)  # Discard line number
                continue
            if section == mips.RE.TEXT_SEC:
                sections[section].append((lineno, line))  # Save og line number
                continue
        else:
            section = line

    return sections[mips.RE.DATA_SEC], sections[mips.RE.TEXT_SEC]


def data_labels(labels: lbldict, data_sec: List[str], memory):
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
            labels[name] = Label(
                name=name,
                value=address,
                type=mips.RE.DATA_SEC
            )


def code_labels(
    labels: lbldict,
    text_sec: List[Tuple[int, str]]
) -> List[Tuple[int, str]]:
    """
    Construct the .text section to spec.

    Fill the .text section memory with user code
    """
    from dashmips.instructions import Instructions

    text = []
    lbl_ct = 0
    for idx, linenotpl in enumerate(text_sec):
        lineno, line = linenotpl
        # For each line in the stipped text section, check for label
        match = re.match(f"({mips.RE.LABEL}):", line)
        if match:
            # If there's a label save it to the labels dictionary
            labels[match[1]] = Label(
                type=mips.RE.TEXT_SEC,
                value=(idx - lbl_ct),
                name=match[1]
            )
            if len(line) > len(match[0]):
                # If the line is longer than what was matched, lets assume
                # the rest is an instruction (comments and whitespace should
                # already have been stripped) we cut out the label
                text.append((lineno, line[len(match[0]):].strip()))
            else:
                # To offset the previously removed label lines
                lbl_ct += 1
        else:
            instruction = line.split(' ')[0]
            if instruction not in Instructions:
                print(f'Error line {idx}: "{instruction}" invalid')
                exit(1)
            # Otherwise save the line as is
            text.append((lineno, line))

    # Converting in code labels to values
    for idx, linenotpl in enumerate(text):
        lineno, line = linenotpl
        for name, label in labels.items():
            # For each label modify the string so that the
            # label is replaced with the value
            if name in line:
                text[idx] = (lineno, line.replace(name, str(label.value)))

    return text
