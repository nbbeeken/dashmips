# Dashmips

Dashmips is a Mips Interpreter CLI Program.

## Requirements

Dashmips has no dependencies beyond requiring `python 3.7`.
There is a dataclasses module for python 3.6 that may make this module work but it is untested.

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

or equivalently

```sh
python -m dashmips
```

## Running

```sh
dashmips run FILE.mips
```

> Note: FILE is a positional argument in the run subcommand

## Debugging

In order to leave a flexible environment for debugging dashmips doesn't provide an interface for human debugging of a mips program. Instead the debugger included is a server that accepts the json format of a mips program over the network and will do the requested operations returning an updated MipsProgram json object.

There is a vscode extension that can speak dashmips specific json language [here](https://github.com/nbbeeken/dashmips-debugger).

### Debugger Protocol

The dashmips process loads the program from a file and opens a websocket. The supported commands can be found in dashmips/debug.py as functions prepended with `debug_`.
The protocol loosely follows JSONRPC for the sake of quick development iteration it is not compliant however this could be easily remedied in a future release.

## Contributing

### Getting Setup

If you want to contribute to the dashmips project you will need the following:

- [Poetry](https://poetry.eustace.io/docs/) is used for dependencies, it will help get you up and running
- After installing Poetry, and cloning this repository:
- `poetry install` - will install the dashmips dependencies in a virtual environment that won't harm your global set up.
- `poetry run X` - can run X command in the correct python environment
- Try `poetry run pytest --tap-stream --tap-outdir=testout --mypy --docstyle --codestyle` to ensure all tests are passing correctly

### Adding Syscalls / Adding Instructions

You can add to the existing files in the `dashmips/instructions` and `dashmips/syscalls` directories using the relevant decorator (`@`).
If you add instructions or syscalls to a new file in these subdirectories ensure that the new file is named with the pattern: `*_instructions.py` or `*_syscalls.py` where `*` is whatever identifier you choose.

### Testing environment install

To make sure dashmips installs correctly in a clean environment I've created a dockerfile that sets up the minimal required env for dashmips. The command below can be used to create the image.

```sh
docker build --rm -f "tests\test_env\Dockerfile" -t dashmips_test_env:latest .
```

Happy coding!
