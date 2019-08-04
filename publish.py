#! /usr/bin/env python
"""Run Publish Commands."""
import shutil
import sys
from shlex import split
from subprocess import run

shutil.rmtree("dist", ignore_errors=True)
shutil.rmtree("build", ignore_errors=True)
shutil.rmtree("src/dashmips.egg-info", ignore_errors=True)
shutil.rmtree("src/__pycache__", ignore_errors=True)
shutil.rmtree("src/dashmips/__pycache__", ignore_errors=True)
shutil.rmtree("src/dashmips/syscalls/__pycache__", ignore_errors=True)
shutil.rmtree("src/dashmips/instructions/__pycache__", ignore_errors=True)
shutil.rmtree("src/dashmips/plugins/__pycache__", ignore_errors=True)
shutil.rmtree("tests/__pycache__", ignore_errors=True)
shutil.rmtree("tests/test_code/__pycache__", ignore_errors=True)
shutil.rmtree("tests/debugger/__pycache__", ignore_errors=True)
shutil.rmtree(".mypy_cache", ignore_errors=True)
shutil.rmtree("testout", ignore_errors=True)
shutil.rmtree(".pytest_cache", ignore_errors=True)


if "clean" in sys.argv:
    sys.exit(0)  # Exit before we do anything more

run(split("python setup.py sdist bdist_wheel"), shell=True)
run(split("twine upload dist/*"), shell=True)
