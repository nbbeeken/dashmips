"""Main Dashmips Program."""
import argparse
import sys
import dashmips.run
import dashmips.debugserver
import json
import dashmips.preprocessor
import dashmips.hw as hw
from dashmips.MipsProgram import MipsProgram


def main(args):
    """Entry into dashmips."""
    if args is None:
        args = dashmips_arguments()

    registers = hw.Registers()
    memory = hw.Memory()

    with open(args.FILE) as file:
        rawcode = file.read()
        labels, code = dashmips.preprocessor.preprocess(rawcode, memory)
        program = MipsProgram(args.FILE, labels, code, memory, registers)
        if args.debug:
            dashmips.debugserver.debug_mips(program)
        else:
            dashmips.run.exec_mips(program)


def dashmips_arguments():
    """Parse Dashmips Arguments."""
    parser = argparse.ArgumentParser("dashmips")
    parser.add_argument("FILE")
    parser.add_argument('-d', '--debug', dest='debug',
                        action='store_true', help='run debugger')
    return parser.parse_args(sys.argv[1:])
