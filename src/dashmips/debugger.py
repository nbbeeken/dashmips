"""Mips Debugger.
All commands need to return
{
    result?: {program: MipsProgram, any_key: other_data}
    error?:{code: number, message: str, data?: any}
}
"""
import logging as log
import os
from typing import Dict, List, Callable, Optional, Any
from dataclasses import asdict
from json import JSONDecoder, JSONEncoder

from .mips import MipsException
from .run import next_instruction, run
from .models import MipsProgram, DebugMessage


def debug_start(program: MipsProgram, params) -> dict:
    """Debug start.

    :param operation: dict
    :param program: MipsProgram
    """
    program.registers["pc"] = program.labels["main"].value
    return {'result': {
        'pid': os.getpid(),
    }}


def debug_step(program: MipsProgram, params) -> dict:
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
    return {'result': {}}


def debug_continue(program: MipsProgram, params) -> dict:
    """Debug continue.

    :param operation: dict
    :param program: MipsProgram
    """
    starting_pc = program.registers["pc"]
    # vscode should have done the translation
    # these are pc values (aka index into srclines)
    breakpoints: List[int] = [p for p in params]

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
            return {'result': {'exited': True}}
    except MipsException as exc:
        error = True
        message = exc.message

    return {'result': {'stopped': True, 'breakpoints': []}}


def debug_stop(program: MipsProgram, params) -> dict:
    """Stop messages incoming mean nothing to a server.

    :param operation: dict
    :param program: MipsProgram
    """
    return {'result': {'exited': True}}


def debug_info(program: MipsProgram, params) -> dict:
    """Build program as dict."""
    return {'result': {
        'program': program.to_dict()
    }}
