"""dashmips program."""

import argparse
from dashmips.parser import exec_mips


def main(args):
    """Entry into dashmips."""
    with open(args.FILE) as file:
        mips_code = file.read()
        exec_mips(mips_code)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("dashmips")
    parser.add_argument("FILE")
    main(parser.parse_args())
