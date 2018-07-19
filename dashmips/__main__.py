"""
dashmips
"""

import argparse
from dashmips.parser import MIPSParser


def main(args):
    string = """.data
msg: .asciiz "Hello World"
.text
        li $v0, 4       # syscall 4 (print_str)
        la $a0, msg     # argument: string
        syscall         # print the string
        lw $t1, foobar
        jr $ra          # retrun to caller"""
    MIPSParser().parse(string)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("dashmips")
    parser.add_argument("FILE")
    main(parser.parse_args())
