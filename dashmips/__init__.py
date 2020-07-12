"""dashmips package."""

import os as _os
from importlib import import_module as _import_module

_DASH_HOME = _os.path.dirname(_os.path.abspath(__file__))

# Import all instructions
_instr_filter = lambda fn: fn.endswith("_instructions.py")
_instr_files = _os.listdir(_os.path.join(_DASH_HOME, "instructions"))
_instr_files = filter(_instr_filter, _instr_files)  # type: ignore
_instr_modules = [f"dashmips.instructions.{mn[:-3]}" for mn in _instr_files]

for _im in _instr_modules:
    _import_module(_im)

# Import all syscalls
_syscall_filter = lambda fn: fn.endswith("_syscalls.py")
_syscall_files = _os.listdir(_os.path.join(_DASH_HOME, "syscalls"))
_syscall_files = filter(_syscall_filter, _syscall_files)  # type: ignore
_syscall_modules = [f"dashmips.syscalls.{mn[:-3]}" for mn in _syscall_files]

for _sm in _syscall_modules:
    _import_module(_sm)

__all__ = ["syscalls", "instructions", "plugins", "directives", "hardware", "mips", "models", "preprocessor", "run", "debugger", "debuggerserver"]
