"""dashmips program."""
import argparse
import json
from threading import Thread
from typing import Any, List, NoReturn

from .debuggerserver import debug_mips
from .extension import generate_snippets, instruction_name_regex
from .plugins.vt100 import VT100
from .preprocessor import preprocess


def main_compile(args: argparse.Namespace) -> int:
    """Compile/Exec mips code."""
    if args.file:
        program = preprocess(args.file)
    if args.out:
        json.dump(program.to_dict(), args.out)

    if args.json:
        # Ending matches socket communication
        print(json.dumps(program.to_dict()))

    if args.vscode:
        snippets = generate_snippets()
        print(json.dumps(snippets, indent=4))
        print("\n\n\n")
        print(instruction_name_regex())

    return 0


def main_run(args: argparse.Namespace) -> int:
    """Run for exec-ing mips program."""
    from .run import run

    program = preprocess(args.FILE, args=args.mips_args)
    plugins: List[Any] = []
    if args.vt100:
        vt = VT100()  # type: ignore
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
    program = preprocess(args.FILE, args=args.mips_args)
    debug_mips(program, args.host, args.port, should_log=args.log)
    return 0


def main_docs(args: argparse.Namespace) -> int:
    """Display information about mips."""
    from .instructions import Instructions
    from .syscalls import Syscalls

    # Syscall printer
    print("Syscalls")
    print(f"{'name':15}{'number':<10}{'description'}")
    print(f"{'----':15}{'------':<10}{'-----------'}")
    syscalls_list = list(Syscalls.items())
    syscalls_list.sort(key=lambda i: i[0])
    for sys_num, syscall in syscalls_list:
        print(f"{syscall.name:15}{sys_num:<10}{syscall.description}")

    print()

    # Instructions printer
    print("Instructions")
    print(f"{'format':<35}{'description'}")
    print(f"{'------':<35}{'-----------'}")
    snips = generate_snippets(examples=True)
    instr_list = list(Instructions.items())
    instr_list.sort(key=lambda i: i[0])
    for instrname, instruction in instr_list:
        ex_str = snips[instrname]["example"]
        desc = snips[instrname]["description"]
        print(f"{ex_str:35}# ", end="")
        print(f"{desc}")

    return 0


def main() -> NoReturn:
    """Entry function for Dashmips."""
    parser = argparse.ArgumentParser("dashmips")

    parser.add_argument("-v", "--version", action="version", version="0.0.11")

    sbp = parser.add_subparsers(title="commands", dest="command")
    compileparse = sbp.add_parser("compile", aliases=["c"])
    runparse = sbp.add_parser("run", aliases=["r"])
    debugparse = sbp.add_parser("debug", aliases=["d"])
    docsparse = sbp.add_parser("docs", aliases=["h"])

    compileparse.add_argument("-f", "--file", type=argparse.FileType("r", encoding="utf8"), help="Input file")
    compileparse.add_argument("-o", "--out", type=argparse.FileType("w", encoding="utf8"), help="Output file name")
    compileparse.add_argument("-j", "--json", action="store_true", help="Output json to stdout")
    compileparse.add_argument("--vscode", action="store_true", help="Output json for vscode")
    compileparse.set_defaults(func=main_compile)

    runparse.add_argument("FILE", type=argparse.FileType("r", encoding="utf8"), help="Input file")
    runparse.add_argument("-a", "--args", dest="mips_args", nargs="*", help="Arguments to pass into the mips main")
    runparse.add_argument("-t", "--vt100", action="store_true", help="Start VT100 Simulator")
    runparse.set_defaults(func=main_run)

    debugparse.add_argument("FILE", type=argparse.FileType("r", encoding="utf8"), help="Input file")
    debugparse.add_argument("-a", "--args", dest="mips_args", nargs="*", help="Arguments to pass into the mips main")
    debugparse.add_argument("-t", "--vt100", action="store_true", help="Start VT100 Simulator")
    debugparse.add_argument("-p", "--port", type=int, default=2390, help="run debugger on port")
    debugparse.add_argument("-i", "--host", default="0.0.0.0", help="run debugger on host")
    debugparse.add_argument("-l", "--log", dest="log", action="store_true", help="Log all network traffic")
    debugparse.set_defaults(func=main_debug)

    docsparse.add_argument("-s", "--syscalls", action="store_true", help="Show syscall table")
    docsparse.add_argument("-i", "--instr", action="store_true", help="Show instruction table")
    docsparse.set_defaults(func=main_docs)

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
    main()
