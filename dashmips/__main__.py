"""dashmips program."""
from dashmips.preprocessor import preprocess, MipsProgram
from dashmips.debugserver import debug_mips

def main_compile(args):
    """Compile/Exec mips code."""
    program = preprocess(args.FILE)
    if args.out:
        program.dump(args.out)

    if args.json:
        print(program.dumps(), end='\r\n\r\n')  # Ending matches socket comm

    if args.run:
        from dashmips.run import run
        run(program)

    return 0


def main_debug(args):
    """Start debug server for mips."""
    debug_mips(host=args.host, port=args.port)


if __name__ == "__main__":
    import argparse
    import sys
    parser = argparse.ArgumentParser('dashmips')

    sbp = parser.add_subparsers(title='commands', dest='command', required=True)
    compileparse = sbp.add_parser('compile', aliases=['c'])
    debugparse = sbp.add_parser('debug', aliases=['d'])

    compileparse.add_argument(
        'FILE',
        type=argparse.FileType('r', encoding='utf8'), help='Input file',
    )
    compileparse.add_argument(
        '-r', '--run', action='store_true', help='Exec input file'
    )
    compileparse.add_argument(
        '-o', '--out',
        type=argparse.FileType('w', encoding='utf8'), help='Output file name'
    )
    compileparse.add_argument(
        '-j', '--json', action='store_true', help='Output json to stdout'
    )
    compileparse.set_defaults(func=main_compile)

    debugparse.add_argument(
        '-p', '--port', type=int, default=9999, help='run debugger on port'
    )
    debugparse.add_argument(
        '-i', '--host', default='localhost', help='run debugger on host'
    )
    debugparse.set_defaults(func=main_debug)

    prog_args = parser.parse_args()
    sys.exit(prog_args.func(prog_args))
