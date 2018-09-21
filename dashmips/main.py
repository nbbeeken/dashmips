"""Main Dashmips Program."""
import argparse
import sys
import dashmips.run
import json
import dashmips.preprocessor
import dashmips.hw as hw


def main(args):
    """Entry into dashmips."""
    if args is None:
        args = dashmips_arguments()

    registers = hw.Registers()
    memory = hw.Memory()

    with open(args.FILE) as file:
        rawcode = file.read()
        labels, code_data = dashmips.preprocessor.preprocess(rawcode, memory)
        dashmips.run.exec_mips(labels, code_data, registers, memory)


def dashmips_arguments():
    """Parse Dashmips Arguments."""
    parser = argparse.ArgumentParser("dashmips")
    parser.add_argument("FILE")
    return parser.parse_args(sys.argv[1:])
