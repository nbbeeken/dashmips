"""dashmips package."""

import os as _os
from importlib import import_module as _import_module

# Import all instructions
_instruction_filter = (lambda fn: fn.endswith("_instructions.py"))
_instruction_files = _os.listdir(
    _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "instructions")
)
_instruction_files = filter(_instruction_filter, _instruction_files)
_instruction_modules = [
    f"dashmips.instructions.{mn[:-3]}" for mn in _instruction_files
]

for _im in _instruction_modules:
    _import_module(_im)

# Import all syscalls
_syscall_filter = (lambda fn: fn.endswith("_instructions.py"))
_syscall_files = _os.listdir(
    _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "syscalls")
)
_syscall_modules = [
    f"dashmips.syscalls.{mn[:-3]}" for mn in _instruction_files
]

for _sm in _syscall_modules:
    _import_module(_sm)

__all__ = [
    'syscalls', 'instructions', 'plugins', 'directives', 'hardware', 'mips',
    'models', 'preprocessor', 'run', 'debugger', 'debuggerwsserver'
]
