"""Tests for Mips Debug Server."""
from typing import Dict, Any, cast

import json
import unittest
from pprint import pformat
from shlex import split
from socket import socket
from subprocess import PIPE, Popen, run
from time import sleep

SERVER = Popen(split("python -m dashmips debug -l"))
sleep(0.1)  # Should be plenty of time to start and bind


def compile_file(filename: str) -> Dict[str, Any]:
    """Run compiler on filename."""
    proc = run(split(f"python -m dashmips c {filename} -j"),
               capture_output=True, encoding='utf8')
    return cast(Dict[str, Any], json.loads(proc.stdout.strip()))


def communicate(msg: Dict[str, Any]) -> Any:
    """Send json encoded message."""
    s = socket()
    s.connect(('localhost', 9999))
    wfile = s.makefile('w', encoding='utf8', buffering=1)
    rfile = s.makefile('r', encoding='utf8', buffering=1)
    wfile.write(json.dumps(msg) + '\r\n')
    wfile.flush()
    received = rfile.readline().strip()
    resp = json.loads(received)
    s.close()
    return resp


def recv() -> Dict[str, Any]:
    """Recv json encoded message."""
    s = socket()
    s.connect(('localhost', 9999))
    rfile = s.makefile('r', encoding='utf8', buffering=1)
    received = rfile.readline().strip()
    resp = json.loads(received)
    s.close()
    return cast(Dict[str, Any], resp)


class TestMipsDebugServer(unittest.TestCase):
    """Testing for mips debug server."""

    def test_start(self):
        """Test start command."""
        program = compile_file('test.mips')

        resp = communicate({'command': 'start', 'program': program})

        program = resp['program']

        self.assertIn('command', resp, pformat(resp))
        self.assertIn('program', resp, pformat(resp))
        self.assertEqual(resp['command'], 'start', pformat(resp))
        self.assertEqual(program['labels']['main']['value'], program['registers']['pc'], pformat(resp))
        self.assertLessEqual(program['registers']['pc'], len(program['source']), pformat(resp))
        self.stop_debugging()

    def stop_debugging(self):
        """Send a proper stop command to the debugger."""
        SERVER.kill()


if __name__ == '__main__':
    try:
        unittest.main()
    finally:
        pass
        SERVER.kill()
