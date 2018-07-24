"""
dashmips
"""

import argparse
from dashmips.parser import exec_mips


def main(args):
    string = """.data
msg: .asciiz "Hello World"
.text
main:
    addi $v0, $zero, 4       # syscall 4 (print_str)
    syscall                  # print the string
    addi $v0, $zero, 10      # load imm hack
    syscall                  # exit"""
    exec_mips(string)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("dashmips")
    parser.add_argument("FILE")
    main(parser.parse_args())
