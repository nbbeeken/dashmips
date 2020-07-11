"""dashmips program."""
import argparse
import json
import sys
from threading import Thread
from typing import Any, List, NoReturn

from .extension import generate_snippets, instruction_name_regex
from .plugins.vt100 import VT100
from .preprocessor import preprocess
from .utils import MipsException


def main_compile(args: argparse.Namespace) -> int:
    """Compile/Exec mips code."""
    program = preprocess(args.FILE)
    if args.out:
        json.dump(program.to_dict(), args.out)
    else:
        print(json.dumps(program.to_dict()))
    return 0


def main_run(args: argparse.Namespace) -> int:
    """Run for exec-ing mips program."""
    from .run import run

    program = preprocess(args.FILE, args=args.mips_args)
    plugins: List[Any] = []
    if args.vt100:
        vt = VT100()
        # program.memory.on_change(vt.push)
        t = Thread(target=run, args=(program,))
        t.start()
        vt.start()
        vt.request_close()
        return 0
    else:
        return run(program)


def main_debug(args: argparse.Namespace) -> int:
    """Start debug server for mips."""
    from .debuggerserver import debug_mips

    program = preprocess(args.FILE, args=args.mips_args)
    debug_mips(program, args.host, args.port, should_log=args.log)
    return 0


def main_docs(args: argparse.Namespace) -> int:
    """Display information about mips."""
    from .instructions import Instructions
    from .syscalls import Syscalls

    print_both = not args.syscalls and not args.instructions
    if print_both or args.syscalls:
        # Syscall printer
        print("Syscalls")
        print(f"{'name':15}{'number':<10}{'description'}")
        print(f"{'----':15}{'------':<10}{'-----------'}")
        syscalls_list = list(Syscalls.items())
        syscalls_list.sort(key=lambda i: i[0])
        for sys_num, syscall in syscalls_list:
            print(f"{syscall.name:15}{sys_num:<10}{syscall.description}")
        print()

    if print_both or args.instructions:
        # Instructions printer
        print("Instructions")
        print(f"{'format':<35}{'description'}")
        print(f"{'------':<35}{'-----------'}")
        snippets = generate_snippets(examples=True)
        instr_list = list(Instructions.items())
        instr_list.sort(key=lambda i: i[0])
        for instrname, instruction in instr_list:
            ex_str = snippets[instrname]["example"]
            desc = snippets[instrname]["description"]
            print(f"{ex_str:35}# ", end="")
            print(f"{desc}")

    return 0


def main_utils(args: argparse.Namespace) -> int:
    """General utilities to help a mips developer."""
    if args.snippets:
        snippets = generate_snippets()
        print(json.dumps(snippets, indent=4))
    if args.instruction_regex:
        print(instruction_name_regex())
    return 0


def main() -> NoReturn:
    """Entry function for Dashmips."""
    parser = argparse.ArgumentParser("dashmips")

    parser.add_argument("-v", "--version", action="version", version="0.1.0")

    sbp = parser.add_subparsers(title="commands", dest="command")
    compileparse = sbp.add_parser("compile", aliases=["c"])
    runparse = sbp.add_parser("run", aliases=["r"])
    debugparse = sbp.add_parser("debug", aliases=["d"])
    docsparse = sbp.add_parser("docs", aliases=["h"])
    utilsparse = sbp.add_parser("utils", aliases=["u"])

    compileparse.add_argument("FILE", type=argparse.FileType("r", encoding="utf8"), help="Input file")
    compileparse.add_argument("-o", "--out", type=argparse.FileType("w", encoding="utf8"), help="Output file name")
    compileparse.set_defaults(func=main_compile)

    runparse.add_argument("FILE", type=argparse.FileType("r", encoding="utf8"), help="Input file")
    runparse.add_argument("-a", "--args", dest="mips_args", nargs="*", help="Arguments to pass into the mips main")
    runparse.add_argument("--vt100", action="store_true", help="Start VT100 Simulator")
    runparse.set_defaults(func=main_run)

    debugparse.add_argument("FILE", type=argparse.FileType("r", encoding="utf8"), help="Input file")
    debugparse.add_argument("-a", "--args", dest="mips_args", nargs="*", help="Arguments to pass into the mips main")
    debugparse.add_argument("--vt100", action="store_true", help="Start VT100 Simulator")
    debugparse.add_argument("-p", "--port", type=int, default=2390, help="run debugger on port")
    debugparse.add_argument("-i", "--host", default="0.0.0.0", help="run debugger on host")
    debugparse.add_argument("-l", "--log", dest="log", action="store_true", help="Log all network traffic")
    debugparse.set_defaults(func=main_debug)

    docsparse.add_argument("-s", "--syscalls", action="store_true", help="Show syscall table")
    docsparse.add_argument("-i", "--instructions", action="store_true", help="Show instruction table")
    docsparse.set_defaults(func=main_docs)

    utilsparse.add_argument("--snippets", action="store_true", help="Output snippets json")
    utilsparse.add_argument("--instruction_regex", action="store_true", help="Output regex that matches instructions")
    utilsparse.set_defaults(func=main_utils)

    prog_args = parser.parse_args()
    if not hasattr(prog_args, "func"):
        # This is for python 3.6 compatibility
        # you cannot enforce subparser to require in less than 3.6
        print("Must provide a command")
        parser.print_help()
        exit(1)

    ret_val = prog_args.func(prog_args)
    exit(ret_val)


if __name__ == "__main__":
    try:
        main()
    except MipsException as ex:
        # All known errors should be caught and re-raised as MipsException
        # If a user encounters a traceback that should be a fatal issue
        print("dashmips encountered an error!", file=sys.stderr)
        print(ex, file=sys.stderr)
    except KeyboardInterrupt as ex:
        # Program should be closed
        print("Program terminated.", file=sys.stderr)
        sys.exit()
