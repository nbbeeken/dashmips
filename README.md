# Dashmips

Dashmips is a Mips Interpreter CLI Program.

## Install

The recommended way to install dashmips is with pip:

```sh
pip install dashmips
```

## Usage

If you installed via pip you should now have a binary in your path that you can launch by typing:

```sh
dashmips
```

## "Compiling"

To compile or run a mips program you run:

```sh
dashmips compile -f FILE.mips
```

What "compilation" means in dashmips is a conversion of the source file to a json format that is better understood by the program. You can use this json format to inspect the internals of how your mips program is interpretted by dashmips.

## Running

This one's easy:

```sh
dashmips run FILE.mips
```

> Note: FILE is a positional argument in the run subcommand

## Debugging

In order to leave a flexible environment for debugging dashmips doesn't provide an interface for human debugging of a mips program. Instead the debugger included is a server that accepts the json format of a mips program over the network and will do the requested operations returning an updated MipsProgram json object.

There is a vscode extension that can speak dashmips specific json language [here](https://github.com/nbbeeken/dashmips-debugger).

### Debugging protocol

Small notes about the protocol if you want to proceed with a manual debugging. The JSON you send to the debug server is expected to take the following format:

```ts
interface DebugMessage {
    command: 'start' | 'step' | 'continue' | 'stop';
    program: MipsProgram;  // MipsProgram can be found in `dashmips/models.py`
    // properties below are optional
    breakpoints?: number[];
    message?: string;
    error?: boolean;
}
```

The commands listed are `start`, `step`, `continue`, and `stop`. In short each operation does the following:

- Start: sets the pc to the main label
- Step: runs exactly one instruction from current pc
- Continue: runs as many instructions as there are between current pc and a breakpoint
- Stop: Does nothing

The server is designed to be stateless so it can handle many clients at once.

## Contributing

### Adding Syscalls / Adding Instructions

You can add to the existing files in the `dashmips/instructions` and `dashmips/syscalls` directories using the relevant decorator (`@`).
If you add instructions or syscalls to a new file in these subdirectories ensure that the new file is named with the pattern: `*_instructions.py` or `*_syscalls.py` where `*` is whatever identifier you choose.
