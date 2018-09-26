"""Main Dashmips Program."""
import argparse
import sys
import dashmips.run
import dashmips.debugserver
import json
import dashmips.preprocessor as preprocessor
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
        labels, code, sourcemap = preprocessor.preprocess(rawcode, memory)
        program = MipsProgram(args.FILE, labels, code, memory, registers)

        if args.debug:
            dashmips.debugserver.debug_mips(program, sourcemap)
        elif args.json:
            with open(f"{args.FILE}.json", 'w') as outfile:
                import json
                json.dump(
                    {
                        **{
                            key: val for key, val in dict(program).items()
                            if key in ['code', 'labels', 'name', 'memory']
                        },
                        'sourcemap': sourcemap
                    }, outfile, indent=4, ensure_ascii=True,
                )
        else:
            dashmips.run.exec_mips(program)

    sys.exit(0)


def dashmips_arguments():
    """Parse Dashmips Arguments."""
    parser = argparse.ArgumentParser("dashmips")
    parser.add_argument("FILE")
    parser.add_argument('-d', '--debug', dest='debug',
                        action='store_true', help='run debugger')
    parser.add_argument('-j', '--json', dest='json',
                        action='store_true', help='output json repr of mips')
    return parser.parse_args(sys.argv[1:])
