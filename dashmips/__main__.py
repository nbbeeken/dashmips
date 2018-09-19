"""dashmips program."""

import dashmips.parser
import argparse


def main(args):
    """Entry into dashmips."""
    with open(args.FILE) as file:
        mips_code = file.read()
        dashmips.parser.exec_mips(mips_code)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("dashmips")
    parser.add_argument("FILE")
    main(parser.parse_args())
