"""Integration Tests."""

import os
from subprocess import run, PIPE
from shlex import split


TEST_MIPS_DIRECTORY = os.path.dirname(os.path.realpath(__file__))


def run_mips_file(filename: str) -> str:
    """Run mips file."""
    proc = run(split(f"python -m dashmips run {TEST_MIPS_DIRECTORY}/{filename}"), stdout=PIPE, stderr=PIPE, encoding="utf8")
    assert proc.stderr == ""
    assert proc.returncode == 0
    return proc.stdout


def test_args_mips():
    """Test args.mips."""
    stdout = run_mips_file("args.mips")
    assert "argc" in stdout
