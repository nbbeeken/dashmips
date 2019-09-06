#! /usr/bin/env python
"""Run Publish Commands."""
import argparse
import shutil
import sys
import os
from shlex import split
from subprocess import run
from typing import *


def find_all(name: str) -> Iterator[str]:
    """Find all matching files or dirs."""
    for root, dirs, files in os.walk('.'):
        if '.\\.git' in root:
            continue
        if name in files or name in dirs:
            yield os.path.join(root, name)


def main_clean() -> int:
    """Clean project working directory."""
    def rm(file: str): shutil.rmtree(file, ignore_errors=True)
    def rm_all(file: str): [rm(f) for f in find_all(file)]

    rm("dist")
    rm("build")
    rm("testout")
    rm_all("dashmips.egg-info")
    rm_all(".pytest_cache")
    rm_all(".mypy_cache")
    rm_all("__pycache__")
    return 0


def main_publish() -> int:
    """Publish module to pypi."""
    main_clean()
    run(split("poetry build"), shell=True)
    run(split("twine upload dist/*"), shell=True)
    return 0


def main_hooks() -> int:
    """Install git hooks."""
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser('Helpful scripts')

    subparser = parser.add_subparsers(title="commands", dest="command")
    cleancommand = subparser.add_parser("clean", help="clean up working dir")
    publishcommand = subparser.add_parser("publish", help="publish to pypi")
    hookscommand = subparser.add_parser("hooks", help="install git hooks")

    cleancommand.set_defaults(func=main_clean)
    publishcommand.set_defaults(func=main_publish)

    prog_args = parser.parse_args()
    try:
        ret_val = prog_args.func()
        exit(ret_val)
    except AttributeError:
        # This is for python 3.6 compatibility
        # you cannot enforce subparser to require in less than 3.6
        print('Must provide a command')
        parser.print_help()
        sys.exit(1)
