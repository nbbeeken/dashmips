"""Mips Debugger."""
import logging as log
import os
from typing import Dict, List, Callable, Optional, Any
from dataclasses import asdict

from .mips import MipsException
from .run import next_instruction, run
from .models import MipsProgram, DebugMessage


def debug_start(program: MipsProgram, params) -> int:
    """Debug start.

    :param operation: dict
    :param program: MipsProgram
    """
    program.registers["pc"] = program.labels["main"].value
    return {'pid': os.getpid(), 'source': [asdict(s) for s in program.source]}


def debug_step(program: MipsProgram, params) -> MipsProgram:
    """Debug step.

    :param operation: dict
    :param program: MipsProgram
    """
    try:
        next_instruction(program)
        if program.registers["pc"] == -1:
            command = "stop"
    except MipsException as exc:
        error = True
        message = exc.message
    return []


def debug_continue(program: MipsProgram, params) -> MipsProgram:
    """Debug continue.

    :param operation: dict
    :param program: MipsProgram
    """
    starting_pc = program.registers["pc"]
    breakpoints: List[int] = [p['srcLineIdx'] for p in params]

    def breaking_condition(program: MipsProgram) -> bool:
        """Condition function to stop execution.

        :param program:
        """
        nonlocal starting_pc
        if program.registers["pc"] == starting_pc:
            # current instruction will execute even if on breakpoint
            # b/c we would have broken on it last time.
            return True
        if program.registers["pc"] in breakpoints:
            return False
        if program.registers["pc"] == -1:
            return False
        return True

    try:
        run(program, breaking_condition)
        if program.registers["pc"] == -1:
            # Exited
            return {'exited': True}
    except MipsException as exc:
        error = True
        message = exc.message

    return {'stopped': asdict(program.current_line)}


def debug_stop(program: MipsProgram, params) -> MipsProgram:
    """Stop messages incoming mean nothing to a server.

    :param operation: dict
    :param program: MipsProgram
    """
    return []
