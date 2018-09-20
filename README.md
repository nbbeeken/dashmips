# Dashmips

Mips Interpreter Program

## Adding Syscalls / Adding Instructions
You can add to the existing files in the `dashmips/instructions` and `dashmips/syscalls` directories using the relevant decorator (`@`).
If you add instructions or syscalls to a new file in these subdirectories **YOU MUST** add an import of the new file to `dashmips/__init__.py`. Otherwise the instruction/syscall will not be constructed and added to the global list.
