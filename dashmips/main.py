"""Main Dashmips Program."""
import argparse
import sys
import dashmips.parser


def main(args):
    """Entry into dashmips."""
    if args is None:
        args = dashmips_arguments()

    with open(args.FILE) as file:
        mips_code = file.read()
        dashmips.parser.exec_mips(mips_code)


def dashmips_arguments():
    """Parse Dashmips Arguments."""
    parser = argparse.ArgumentParser("dashmips")
    parser.add_argument("FILE")
    return parser.parse_args(sys.argv[1:])
