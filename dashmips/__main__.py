"""dashmips program."""

import mipsparser
import argparse


def main(args):
    """Entry into dashmips."""
    with open(args.FILE) as file:
        mips_code = file.read()
        mipsparser.exec_mips(mips_code)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("dashmips")
    parser.add_argument("FILE")
    main(parser.parse_args())
