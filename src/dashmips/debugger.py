"""Mips Debugger."""
import logging as log
import os
from typing import Dict, List, Callable, Optional, Any

from dashmips.mips import MipsException
from dashmips.run import next_instruction, run
from dashmips.models import MipsProgram, DebugMessage


def debug_start(program: MipsProgram) -> int:
    """Debug start.

    :param operation: dict
    :param program: MipsProgram
    """
    program.registers["pc"] = program.labels["main"].value
    return os.getpid()


def debug_step(program: MipsProgram) -> MipsProgram:
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
    return program


def debug_continue(operation: dict, program: MipsProgram) -> MipsProgram:
    """Debug continue.

    :param operation: dict
    :param program: MipsProgram
    """
    starting_pc = program.registers["pc"]
    breakpoints: List[int] = []  # FIXME: remove once u get ur protocol down!

    def breaking_condition(program: MipsProgram) -> bool:
        """Condition function to stop execution.

        :param program:
        """
        nonlocal starting_pc
        log.info(f"bps: {breakpoints}", extra={"client": ""})
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
            command = "stop"
    except MipsException as exc:
        error = True
        message = exc.message

    return program


def debug_stop(operation: dict, program: MipsProgram) -> MipsProgram:
    """Stop messages incoming mean nothing to a server.

    :param operation: dict
    :param program: MipsProgram
    """
    return program


COMMANDS = {
    "start": debug_start,
    "step": debug_step,
    "continue": debug_continue,
    "stop": debug_stop,
}
