"""Preprocessor for mips assembly."""
import os.path
import re
from typing import Any, Dict, Iterable, List, Optional, TextIO, Tuple, TypeVar

import dashmips.mips as mips
from dashmips.hardware import Memory, Registers
from dashmips.mips import MipsException
from dashmips.models import Label, MipsProgram, SourceLine


def preprocess(file: TextIO, args: Optional[List[str]] = None) -> MipsProgram:
    """Prepare Mips for running.

    Breaks the code into directive and text sections.

    :param file: TextIO:
    """
    filename = os.path.abspath(file.name)
    memory = Memory()

    argv = [filename]
    if args:
        argv.extend(args)

    linesofcode: List[SourceLine] = process_file(file)

    labels: Dict[str, Label] = {}
    # Collect Preproccessor Directives.
    eqvs, linesofcode = preprocessor_directives(linesofcode)

    # Gather .data/.text sections into seperate lists
    unprocessed_labels, unprocessed_code = split_to_sections(linesofcode)

    # First process all the .data labels so they can be replaced in .text
    data_labels(labels, unprocessed_labels, memory)
    # Second gather the code labels,
    # this also replaces all labels in code with the correct value
    processed_code = code_labels(labels, unprocessed_code)

    # Cannot run a program without a main
    if not ("main" in labels and labels["main"].location == mips.RE.TEXT_SEC):
        raise Exception(f"Cannot locate main in {filename}")

    bp = memory.malloc(512) + 508
    init_regs = {"pc": labels["main"].value, "$sp": bp, "$fp": bp, "$gp": bp}

    load_args(init_regs, memory, argv)

    return MipsProgram(
        name=filename,
        labels=labels,
        memory=memory,
        source=processed_code,
        registers=Registers(init_regs),
        eqvs=eqvs,
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


def data_labels(labels: Dict[str, Label],
                data_sec: List[str], memory: Memory) -> None:
    """Construct the .data section to spec.

    Fill the .data section memory with user defined static data

    :param labels:
    :param data_sec:
    :param memory:
    """
    data_line_re = f"({mips.RE.LABEL}):\\s*({mips.RE.DIRECTIVE})\\s+(.*)"
    for line in data_sec:
        match = re.match(data_line_re, line)
        if match:
            name = match[1]
            directive = mips.Directives[match[2][1:]]
            address = directive(name, match[3], memory)
            labels[name] = Label(name=name,
                                 value=address,
                                 location=mips.RE.DATA_SEC,
                                 kind=match[2][1:])


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
                location=mips.RE.TEXT_SEC,
                value=(idx - lbl_ct),
                name=match[1],
                kind="text",
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
            instruction = srcline.line.split(" ")[0]
            if instruction not in Instructions:
                print(f'Error line {idx}: "{instruction}" invalid')
                exit(1)
            # Otherwise save the line as is
            text.append(srcline)

    return text


def process_file(file: TextIO) -> List[SourceLine]:
    """Process Mips File.

    :param file: Mips source file
    """
    filename = os.path.abspath(file.name)
    code = file.read()
    linenumbers = list(enumerate(code.splitlines()))
    # remove comments
    nocomments: Iterable[SourceLine] = map(
        lambda ln: SourceLine(
            filename, ln[0] + 1, re.sub(mips.RE.COMMENT, "", ln[1]).strip()
        ),
        linenumbers,
    )
    # drop lines that are empty
    noemptylines: Iterable[SourceLine] = filter(
        lambda ln: ln.line != "", nocomments)

    def manyspaces_to_onespace(ln: SourceLine) -> SourceLine:
        ln.line = " ".join(ln.line.split())
        return ln

    # make every white space just one space
    linesofcode: List[SourceLine] = list(
        map(manyspaces_to_onespace, noemptylines))

    return linesofcode


def preprocessor_directives(
    lines: List[SourceLine]
) -> Tuple[Dict[str, str], List[SourceLine]]:
    """Preprocessor Directives handler.

    :param lines: lines to compile.
    """
    for idx, srcline in enumerate(lines):
        if ".globl" in srcline.line:
            del lines[idx]
    lines = resolve_include(lines)
    lines, eqvs = resolve_eqvs(lines)
    lines = resolve_macros(lines)
    return eqvs, lines


def resolve_include(lines: List[SourceLine]) -> List[SourceLine]:
    """Resolve all includes recursively."""
    for idx, srcline in enumerate(lines):
        match = re.match(r'\s*\.include\s+"(.*)"\s*', srcline.line)
        if match:
            includefilename = os.path.abspath(match[1])
            includefile = open(includefilename)
            includelines = resolve_include(process_file(includefile))
            lines[idx] = includelines  # type: ignore

    lines = flatten(lines)

    return lines


T = TypeVar("T")


def flatten(nestedlist: Iterable[T]) -> List[T]:
    """Flatten a nested list."""
    newlist = []
    for item in nestedlist:
        if isinstance(item, list):
            newlist.extend(flatten(item))
        else:
            newlist.append(item)
    return newlist


def resolve_eqvs(lines: List[SourceLine]
                 ) -> Tuple[List[SourceLine], Dict[str, str]]:
    """Gather eqvs to text replace throughout code."""
    eqvs = {}
    to_del = []
    for idx, srcline in enumerate(lines):
        # Check for eqv on this line
        match = re.match(mips.RE.EQVS, srcline.line)
        if match:
            # Save Eqv into dict
            eqvs[match[1]] = match[2]
            # Delete the eqv line
            to_del.append(idx)

    lines = [l for i, l in enumerate(lines) if i not in to_del]

    for idx, srcline in enumerate(lines):
        # for each line
        for eqv in eqvs.keys():
            # check each eqv and attempt a replacement
            srcline.line = srcline.line.replace(eqv, eqvs[eqv])

    return lines, eqvs


def resolve_macros(lines: List[SourceLine]) -> List[SourceLine]:
    """Find and substitute macros."""
    macros: Dict[str, Dict[str, Any]] = {}
    found_macro = None
    lines_to_remove = []
    for idx, srcline in enumerate(lines):
        if found_macro is None:
            match = re.match(mips.RE.MACRO, srcline.line)
            if match:
                found_macro = match[1]
                macros[match[1]] = {
                    "args": [a.strip() for a in match[2].split(", ")]
                    if match[2]
                    else None,
                    "lines": [],
                }
                lines_to_remove.append(idx)
        else:
            if ".end_macro" in srcline.line:
                found_macro = None
                lines_to_remove.append(idx)
            else:
                macros[found_macro]["lines"].append(srcline)
                lines_to_remove.append(idx)

    lines = [l for i, l in enumerate(lines) if i not in lines_to_remove]

    for idx, srcline in enumerate(lines):
        for macro, macro_info in macros.items():
            if macro in srcline.line:
                if macro_info["args"] is None:
                    lines[idx] = macro_info["lines"]
                else:
                    macro_with_args(idx, lines, macro, macro_info, srcline)

    return flatten(lines)


def macro_with_args(
    idx: int,
    lines: List[SourceLine],
    macro: str,
    macroinfo: Dict[str, Any],
    srcline: SourceLine,
) -> None:
    """Handle Parsing for macro that has arguments."""
    macroregex = fr"{macro}\((.+)\)"
    match = re.match(macroregex, srcline.line)
    if match:
        values = match[1].split(", ")
        argsmap = {arg: val for arg, val in zip(macroinfo["args"], values)}
        expanded_macro = []
        for s in macroinfo["lines"]:
            modified_line = s.line
            for a, v in argsmap.items():
                modified_line = modified_line.replace(a, v)
            expanded_macro.append(
                SourceLine(
                    line=modified_line,
                    lineno=s.lineno,
                    filename=s.filename))
        lines[idx] = expanded_macro  # type: ignore


def load_args(init_regs: Dict[str, int],
              memory: Memory, args: List[str]) -> None:
    """Load arguments on to the stack and sets argc."""
    init_regs["$a0"] = len(args)  # argc

    argv: List[int] = []
    for arg in args:
        ptr = memory.malloc(len(arg) + 1)
        # str ending in null
        memory[ptr: ptr + len(arg) + 1] = [*[ord(c) for c in arg], 0]
        argv.append(ptr)

    argv.append(0)  # NULL to end pointer array

    # Malloc all at once this time for contiguous memory
    argvbp = memory.malloc(len(argv) * 4)

    for idx, ptr in enumerate(argv):
        store_addr = argvbp + idx * 4
        memory[store_addr: store_addr + 4] = ptr.to_bytes(4, "big")

    init_regs["$a1"] = argvbp  # argv
