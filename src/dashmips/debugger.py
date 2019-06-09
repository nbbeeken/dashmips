"""Mips Debugger."""
import logging as log
import os
from typing import Dict, Callable, Optional

from dashmips.debugserver import DebugMessage
from dashmips.mips import MipsException
from dashmips.run import next_instruction, run
from dashmips.models import MipsProgram


def debug_start(msg: DebugMessage) -> Optional[DebugMessage]:
    """Debug start.

    :param msg: DebugMessage:
    """
    msg.program.registers["pc"] = msg.program.labels["main"].value
    msg.message = str(os.getpid())
    return msg


def debug_step(msg: DebugMessage) -> DebugMessage:
    """Debug step.

    :param msg: DebugMessage:
    """
    try:
        next_instruction(msg.program)
        if msg.program.registers["pc"] == -1:
            msg.command = "stop"
    except MipsException as exc:
        msg.error = True
        msg.message = exc.message

    return msg


def debug_continue(msg: DebugMessage) -> DebugMessage:
    """Debug continue.

    :param msg: DebugMessage:
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


def debug_stop(msg: DebugMessage) -> DebugMessage:
    """Stop messages incoming mean nothing to a server.

    :param msg: DebugMessage:
    """
    return msg


Commands: Dict[str, Callable] = {
    "start": debug_start,
    "step": debug_step,
    "continue": debug_continue,
    "stop": debug_stop,
}
