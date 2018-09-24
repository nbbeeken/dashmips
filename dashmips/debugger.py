"""Mips Debugger."""
from typing import Dict, Callable, Optional
from dashmips.debugserver import DebugMessage


def debug_start(program, command: DebugMessage) -> Optional[DebugMessage]:
    """Debug start."""
    program.registers['pc'] = program.labels['main'].value
    return DebugMessage(
        command=command.command,
        value=program.to_dict()
    )


def debug_step(program, command: DebugMessage) -> Optional[DebugMessage]:
    """Debug step."""
    pass


def debug_setbreakpoint(program,
                        command: DebugMessage) -> Optional[DebugMessage]:
    """Debug setbreakpoint."""
    pass


def debug_delbreakpoint(program,
                        command: DebugMessage) -> Optional[DebugMessage]:
    """Debug delbreakpoint."""
    pass


def debug_continue(program, command: DebugMessage) -> Optional[DebugMessage]:
    """Debug continue."""
    pass


def debug_lines(program, command: DebugMessage) -> Optional[DebugMessage]:
    """Debug lines."""
    pass


def debug_breakpoints(program,
                      command: DebugMessage) -> Optional[DebugMessage]:
    """Debug breakpoints."""
    pass


def debug_stepreverse(program,
                      command: DebugMessage) -> Optional[DebugMessage]:
    """Debug stepreverse."""
    pass


def debug_stop(program, command: DebugMessage) -> Optional[DebugMessage]:
    """Debug stop."""
    pass


def debug_registers(program, command: DebugMessage) -> Optional[DebugMessage]:
    """Debug registers."""
    pass


def debug_memory(program, command: DebugMessage) -> Optional[DebugMessage]:
    """Debug memory."""
    pass


def debug_restart(program, command: DebugMessage) -> Optional[DebugMessage]:
    """Debug restart."""
    pass


Commands: Dict[str, Callable] = {
    'start': debug_start,
    'step': debug_step,
    'setbreakpoint': debug_setbreakpoint,
    'delbreakpoint': debug_delbreakpoint,
    'continue': debug_continue,
    'lines': debug_lines,
    'breakpoints': debug_breakpoints,
    'stepreverse': debug_stepreverse,
    'stop': debug_stop,
    'registers': debug_registers,
    'memory': debug_memory,
    'restart': debug_restart,
}
