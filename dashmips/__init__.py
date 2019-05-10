"""dashmips package."""

import os
import os.path
from importlib import import_module

# Import all instructions

instruction_modules = [
    f"dashmips.instructions.{s[:-3]}"
    for s in os.listdir(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "instructions"
        )
    )
    if s.endswith("_instructions.py")
]

for im in instruction_modules:
    import_module(im)

# Import all syscalls

syscall_modules = [
    f"dashmips.syscalls.{s[:-3]}"
    for s in os.listdir(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "syscalls")
    )
    if s.endswith("_syscalls.py")
]

for sm in syscall_modules:
    import_module(sm)
