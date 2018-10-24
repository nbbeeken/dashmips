"""dashmips program."""
import argparse
import json
from threading import Thread
from typing import NoReturn, List, Any

from dashmips.debugserver import debug_mips
from dashmips.extension import generate_snippets, instruction_name_regex
from dashmips.plugins.vt100 import VT100
from dashmips.preprocessor import preprocess


def main_compile(args: argparse.Namespace) -> int:
    """Compile/Exec mips code.

    :param args:
    """
    program = preprocess(args.FILE)
    if args.out:
        json.dump(program.to_dict(), args.out)

    if args.json:
        # Ending matches socket communication
        print(json.dumps(program.to_dict()))

    if args.vscode:
        snippets = generate_snippets()
        print(json.dumps(snippets, indent=4))
        print('\n\n\n')
        print(instruction_name_regex())

    if args.run:
        from dashmips.run import run
        plugins: List[Any] = []
        if args.vt100:
            vt = VT100()
            program.memory.on_change(vt.push)
            t = Thread(target=run, args=(program,))
            t.start()
            vt.start()
            vt.request_close()
        else:
            run(program)

    return 0


def main_debug(args: argparse.Namespace) -> int:
    """Start debug server for mips.

    :param args:

    """
    debug_mips(host=args.host, port=args.port, should_log=args.log)
    return 0


def main() -> NoReturn:
    """Entry function for Dashmips."""
    import sys
    parser = argparse.ArgumentParser('dashmips')

    parser.add_argument('-v', '--version', action='version', version='0.0.1')

    sbp = parser.add_subparsers(
        title='commands', dest='command', required=True
    )
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
    compileparse.add_argument(
        '--vscode', action='store_true', help='Output json for vscode'
    )
    compileparse.add_argument(
        '-t', '--vt100', action='store_true',
        help='Start VT100 Simulator'
    )
    compileparse.set_defaults(func=main_compile)

    debugparse.add_argument(
        '-p', '--port', type=int, default=9999, help='run debugger on port'
    )
    debugparse.add_argument(
        '-i', '--host', default='0.0.0.0', help='run debugger on host'
    )
    debugparse.add_argument(
        '-l', '--log', dest='log',
        action='store_true', help='Log all network traffic'
    )
    debugparse.set_defaults(func=main_debug)

    prog_args = parser.parse_args()
    sys.exit(prog_args.func(prog_args))


if __name__ == "__main__":
    main()
