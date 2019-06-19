"""Mips Debugger."""
import logging as log
import os
from typing import Dict, Callable, Optional

from dashmips.debugserver import DebugMessage
from dashmips.mips import MipsException
from dashmips.run import next_instruction, run
from dashmips.models import MipsProgram


def debug_start(operation: dict, program: MipsProgram) -> dict:
    """Debug start.

    :param operation: dict
    :param program: MipsProgram
    """
    msg.program.registers["pc"] = msg.program.labels["main"].value
    msg.message = str(os.getpid())
    return msg


def debug_step(operation: dict, program: MipsProgram) -> dict:
    """Debug step.

    :param operation: dict
    :param program: MipsProgram
    """
    try:
        next_instruction(msg.program)
        if msg.program.registers["pc"] == -1:
            msg.command = "stop"
    except MipsException as exc:
        msg.error = True
        msg.message = exc.message

    return msg


def debug_continue(operation: dict, program: MipsProgram) -> dict:
    """Debug continue.

    :param operation: dict
    :param program: MipsProgram
    """
    starting_pc = msg.program.registers["pc"]

    def breaking_condition(program: MipsProgram) -> bool:
        """Condition function to stop execution.

        :param program:
        """
        nonlocal starting_pc
        log.info(f"bps: {msg.breakpoints}", extra={"client": ""})
        if program.registers["pc"] == starting_pc:
            # current instruction will execute even if on breakpoint
            # b/c we would have broken on it last time.
            return True
        if program.registers["pc"] in msg.breakpoints:
            return False
        if program.registers["pc"] == -1:
            return False
        return True

    try:
        run(msg.program, breaking_condition)
        if msg.program.registers["pc"] == -1:
            # Exited
            msg.command = "stop"
    except MipsException as exc:
        msg.error = True
        msg.message = exc.message

    return msg


def debug_stop(operation: dict, program: MipsProgram) -> dict:
    """Stop messages incoming mean nothing to a server.

    :param operation: dict
    :param program: MipsProgram
    """
    return msg


COMMANDS: Dict[str, Callable[[dict, MipsProgram], dict]] = {
    "start": debug_start,
    "step": debug_step,
    "continue": debug_continue,
    "stop": debug_stop,
}
