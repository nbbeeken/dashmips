"""Mips Debugger."""
import re
from typing import Dict, Callable, Optional

from dashmips.debugserver import DebugMessage
from dashmips.run import next_instruction, run
from dashmips.mips import MipsException


def debug_start(msg: DebugMessage) -> Optional[DebugMessage]:
    """Debug start."""
    msg.program.registers['pc'] = msg.program.labels['main'].value
    return msg


def debug_step(msg: DebugMessage) -> DebugMessage:
    """Debug step."""
    try:
        next_instruction(msg.program)
        # TODO: Should be doing something with breakpoints here
    except MipsException as exc:
        msg.error = True
        msg.message = exc.message

    return msg


def debug_continue(msg: DebugMessage) -> DebugMessage:
    """Debug continue."""
    starting_pc = msg.program.registers['pc']

    def breaking_condition(program):
        nonlocal starting_pc
        if program.registers['pc'] == starting_pc:
            # current instruction will execute even if on breakpoint
            # b/c we would have broken on it last time.
            return True
        if program.registers['pc'] in msg.breakpoints:
            return False
        return True
    try:
        run(msg.program, breaking_condition)
    except MipsException as exc:
        msg.error = True
        msg.message = exc.message

    return msg


Commands: Dict[str, Callable] = {
    'start': debug_start,
    'step': debug_step,
    'continue': debug_continue,
}
