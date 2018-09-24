"""Mips Debugger."""
import re
from dashmips.instructions import Instructions
from typing import Dict, Callable, Optional
from dashmips.debugserver import DebugMessage


def debug_start(msg: DebugMessage) -> Optional[DebugMessage]:
    """Debug start."""
    msg.program.registers['pc'] = msg.program.labels['main'].value
    return msg


def debug_stop(msg: DebugMessage) -> DebugMessage:
    """Debug stop."""
    return msg


def debug_step(msg: DebugMessage) -> DebugMessage:
    """Debug step."""
    current_pc = msg.program.registers['pc']
    if len(msg.program.code) < current_pc:
        # We jumped or executed beyond available text
        msg.message = 'pc is greater than len(code)'
        msg.error = True
        return msg

    lineofcode = msg.program.code[current_pc]  # Current line of execution
    instruction = lineofcode.split(' ')[0]  # Grab the instruction name

    instruction_fn = Instructions[instruction]  # relevant Instruction()

    match = re.match(instruction_fn.regex, lineofcode)
    if match:
        # Instruction has the correct format
        args = instruction_fn.parser(match)
        instruction_fn(msg.program, args)
    else:
        # Bad arguments to instruction
        msg.message = f"{lineofcode} is malformed for {instruction}"
        msg.error = True
        return msg

    return msg


def debug_setbreakpoints(msg: DebugMessage) -> DebugMessage:
    """Debug setbreakpoint."""
    msg.message = 'Not Implemented'
    msg.error = True
    return msg


def debug_continue(msg: DebugMessage) -> DebugMessage:
    """Debug continue."""
    msg.message = 'Not Implemented'
    msg.error = True
    return msg


def debug_lines(msg: DebugMessage) -> DebugMessage:
    """Debug lines."""
    msg.message = 'Not Implemented'
    msg.error = True
    return msg


def debug_stepreverse(msg: DebugMessage) -> DebugMessage:
    """Debug stepreverse."""
    msg.message = 'Not Implemented'
    msg.error = True
    return msg


def debug_restart(msg: DebugMessage) -> DebugMessage:
    """Debug restart."""
    msg.message = 'Not Implemented'
    msg.error = True
    return msg


Commands: Dict[str, Callable] = {
    'start': debug_start,
    'stop': debug_stop,
    'restart': debug_restart,
    'step': debug_step,
    'stepreverse': debug_stepreverse,
    'setbreakpoints': debug_setbreakpoints,
    'continue': debug_continue,
}
