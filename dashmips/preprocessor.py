"""Preprocessor for mips assembly."""
import json
import re
import os.path
import operator
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Tuple, Optional, TextIO, Iterable

from dashmips.mips import MipsException
import dashmips.mips as mips
from dashmips.hardware import Memory, Registers


@dataclass
class SourceLine:
    """Mips Preprocessor Label."""

    filename: str
    lineno: int
    line: str


@dataclass
class Label:
    """Mips Preprocessor Label."""

    type: str
    value: int
    name: str


@dataclass
class MipsProgram:
    """All data associated with a mips program."""

    name: str
    labels: Dict[str, Label]
    source: List[SourceLine]
    memory: Memory = field(default_factory=Memory)
    registers: Registers = field(default_factory=Registers)

    @staticmethod
    def from_dict(prg) -> 'MipsProgram':
        """From Basic dictionary to MipsProgram.

        :param prg:

        """
        prg['memory'] = Memory(prg['memory'])
        prg['registers'] = Registers(prg['registers'])
        prg['labels'] = {ln: Label(**l) for ln, l in prg['labels'].items()}
        prg['source'] = [SourceLine(**m) for m in prg['source']]
        return MipsProgram(**prg)

    def __iter__(self):
        """Two item iterable for dictionary making."""
        return iter(asdict(self).items())


def preprocess(file: TextIO) -> MipsProgram:
    """Prepare Mips for running.

    Breaks the code into directive and text sections.

    :param file: TextIO:

    """
    filename = os.path.abspath(file.name)
    memory = Memory()

    linesofcode: List[SourceLine] = process_file(file)

    labels: Dict[str, Label] = {}
    # Collect Preproccessor Directives.
    eqvs = preprocessor_directives(linesofcode)

    # Gather .data/.text sections into seperate lists
    unprocessed_labels, unprocessed_code = split_to_sections(linesofcode)

    # First process all the .data labels so they can be replaced in .text
    data_labels(labels, unprocessed_labels, memory)
    # Second gather the code labels,
    # this also replaces all labels in code with the correct value
    processed_code = code_labels(labels, unprocessed_code)

    # Cannot run a program without a main
    assert 'main' in labels and labels['main'].type == mips.RE.TEXT_SEC

    return MipsProgram(
        name=filename,
        labels=labels,
        memory=memory,
        source=processed_code,
        registers=Registers({'pc': labels['main'].value}),
    )


sectionsType = Tuple[List[str], List[SourceLine]]


def split_to_sections(code: List[SourceLine]) -> sectionsType:
    """Handle file with mixed sections.

    .text and .data sections can come in any order.

    :param code: List[Tuple[int:
    :param str]]:

    """
    section: Optional[str] = None
    if code[0].line in [mips.RE.DATA_SEC, mips.RE.TEXT_SEC]:
        section = code[0].line

    if section is None:
        raise MipsException("first line must be .text/.data")

    sections: Dict[str, Any] = {mips.RE.DATA_SEC: [], mips.RE.TEXT_SEC: []}
    for srcline in code:
        if srcline.line not in [mips.RE.DATA_SEC, mips.RE.TEXT_SEC]:
            if section == mips.RE.DATA_SEC:
                sections[section].append(srcline.line)  # Discard line number
                continue
            if section == mips.RE.TEXT_SEC:
                sections[section].append(srcline)  # Save og line number
                continue
        else:
            section = srcline.line

    return sections[mips.RE.DATA_SEC], sections[mips.RE.TEXT_SEC]


def data_labels(labels: Dict[str, Label], data_sec: List[str], memory):
    """Construct the .data section to spec.

    Fill the .data section memory with user defined static data

    :param labels: Dict[str:
    :param Label]:
    :param data_sec: List[str]:
    :param memory:

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
    labels: Dict[str, Label], text_sec: List[SourceLine]
) -> List[SourceLine]:
    """Construct the .text section to spec.

    Fill the .text section memory with user code

    :param labels:
    :param text_sec:
    """
    from dashmips.instructions import Instructions

    text: List[SourceLine] = []
    lbl_ct = 0
    for idx, srcline in enumerate(text_sec):
        # For each line in the stipped text section, check for label
        match = re.match(f"({mips.RE.LABEL}):", srcline.line)
        if match:
            # If there's a label save it to the labels dictionary
            labels[match[1]] = Label(
                type=mips.RE.TEXT_SEC,
                value=(idx - lbl_ct),
                name=match[1]
            )
            if len(srcline.line) > len(match[0]):
                # If the line is longer than what was matched, lets assume
                # the rest is an instruction (comments and whitespace should
                # already have been stripped) we cut out the label
                srcline.line = srcline.line[len(match[0]):].strip()
                text.append(srcline)
            else:
                # To offset the previously removed label lines
                lbl_ct += 1
        else:
            instruction = srcline.line.split(' ')[0]
            if instruction not in Instructions:
                print(f'Error line {idx}: "{instruction}" invalid')
                exit(1)
            # Otherwise save the line as is
            text.append(srcline)

    # Converting in code labels to values
    for idx, srcline in enumerate(text):
        for name, label in labels.items():
            # For each label modify the string so that the
            # label is replaced with the value
            if name in srcline.line:
                srcline.line = srcline.line.replace(name, str(label.value))
                text[idx] = srcline

    return text


def process_file(file):
    """Process Mips File.

    :param file: Mips source file
    """
    filename = os.path.abspath(file.name)
    code = file.read()
    linenumbers = list(enumerate(code.splitlines()))
    # remove comments
    nocomments: Iterable[SourceLine] = map(
        lambda ln: SourceLine(
            filename,
            ln[0] + 1,
            re.sub(mips.RE.COMMENT, '', ln[1]).strip()
        ),
        linenumbers
    )
    # drop lines that are empty
    noemptylines: Iterable[SourceLine] = filter(
        lambda ln: ln.line != '',
        nocomments
    )

    def manyspaces_to_onespace(ln: SourceLine):
        ln.line = ' '.join(ln.line.split())
        return ln

    # make every white space just one space
    linesofcode: List[SourceLine] = list(map(
        manyspaces_to_onespace,
        noemptylines
    ))

    return linesofcode


def preprocessor_directives(lines: List[SourceLine]):
    """Preprocessor Directives handler.

    :param lines: lines to compile.
    """
    directives = ['eqv', 'macro', 'end_macro', 'include']

    newlines = resolve_include(lines)


def resolve_include(lines: List[SourceLine]):
    """Resolve all includes recursively."""
    include_positions = []
    includes = []
    for idx, srcline in enumerate(lines):
        match = re.match(r'\s*\.include\s+"(.*)"\s*', srcline.line)
        if match:
            includefilename = os.path.abspath(match[1])
            includefile = open(includefilename)
            includelines = resolve_include(process_file(includefile))
            includes.append(includelines)
            include_positions.append(idx)

    newlines = []
    idx_includes = enumerate(zip(include_positions, includes))
    for (idx, (include_position, include)) in idx_includes:
        # Next index is either the next include's starting point
        # OR the end of lines
        nextidx = include_positions[idx + 1] if idx + \
            1 < len(include_positions) else len(lines)

        spreads = [
            *lines[0:include_position],  # Spread everything before include
            *include,  # Spread include
            *lines[include_position + 1:nextidx]  # Spread everything after
        ]
        newlines.extend(spreads)

    return newlines
