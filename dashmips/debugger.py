"""Mips Debugger.

All commands need to return
{
    result?: {program: MipsProgram, any_key: other_data}
    error?:{code: number, message: str, data?: any}
}
"""
import os
from typing import List, Dict, Any, Tuple

from .models import MipsProgram
from .run import next_instruction, run
from .utils import MipsException


def debug_start(program: MipsProgram, params=None) -> Dict[str, int]:
    """Debug start."""
    program.registers["pc"] = program.labels["main"].value
    return {"pid": os.getpid()}


def debug_step(program: MipsProgram, params) -> Dict[str, Any]:
    """Debug step."""
    try:
        next_instruction(program)

        if program.exited:
            return {"exited": True}

    except MipsException as exc:
        return {"exited": True, "message": exc.message}

    return {"stopped": True}


def debug_continue(program: MipsProgram, params) -> Dict[str, Any]:
    """Debug continue."""
    starting_pc = program.registers["pc"]
    # vscode should have done the translation
    # these are pc values (aka index into srclines)
    verified, breakpoints = verify_breakpoints(program, params)

    def breaking_condition(program: MipsProgram) -> bool:
        """Condition function to stop execution."""
        nonlocal starting_pc
        if program.registers["pc"] == starting_pc:
            # current instruction will execute even if on breakpoint
            # b/c we would have broken on it last time.
            return True
        if program.registers["pc"] in breakpoints:
            return False
        if program.exited:
            return False
        return True

    try:
        run(program, breaking_condition)
        if program.exited:
            return {"exited": True}
    except MipsException as exc:
        return {"exited": True, "message": exc.message}

    return {"stopped": True, "breakpoints": verified}


def debug_stop(program: MipsProgram, params) -> Dict[str, bool]:
    """Stop messages incoming mean nothing to a server."""
    return {"exited": True}


def debug_info(program: MipsProgram, params) -> Dict[str, Any]:
    """Build program as dict."""
    return {"program": program.to_dict()}


def verify_breakpoints(
    program: MipsProgram, breakpoints
) -> Tuple[List[int], List[int]]:
    """Find the known breakpoint lines."""
    local_breakpoints = []
    remote_breakpoints = []
    for breakpoint in breakpoints:
        def checkfile(f: str) -> bool:
            return os.path.samefile(f, breakpoint["src"]["path"])

        real_line = None
        for pc_value, srcline in enumerate(program.source):
            if breakpoint["line"] == srcline.lineno:
                real_line = pc_value
                break

        is_known_file = any(checkfile(fn) for fn in program.filenames)
        if real_line is not None and is_known_file:
            remote_breakpoints.append(breakpoint["line"])
            local_breakpoints.append(real_line)

    return remote_breakpoints, local_breakpoints
