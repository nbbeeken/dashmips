"""Tests for Mips Debug Server."""
import unittest
from subprocess import Popen, run, PIPE
from shlex import split
from socket import socket
import json
from time import sleep
from pprint import pformat

SERVER = Popen(split("python -m dashmips debug"))
sleep(0.1)  # Should be plenty of time to start and bind


def compile_file(filename):
    """run compiler on filename."""
    proc = run(split(f"python -m dashmips c {filename} -j"),
               capture_output=True, encoding='utf8')
    return json.loads(proc.stdout.strip())


def communicate(msg):
    """Send json encoded message."""
    s = socket()
    s.connect(('localhost', 9999))
    wfile = s.makefile('w', encoding='utf8', buffering=1)
    rfile = s.makefile('r', encoding='utf8', buffering=1)
    wfile.write(json.dumps(msg) + '\r\n')
    wfile.flush()
    recvd = rfile.readline().strip()
    resp = json.loads(recvd)
    s.close()
    return resp


def recv():
    """Recv json encoded message."""
    s = socket()
    s.connect(('localhost', 9999))
    rfile = s.makefile('r', encoding='utf8', buffering=1)
    recvd = rfile.readline().strip()
    resp = json.loads(recvd)
    s.close()
    return resp


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
        self.assertEqual(
            program['labels']['main']['value'],
            program['registers']['pc'],
            pformat(resp),
        )
        self.assertLessEqual(
            program['registers']['pc'],
            len(program['source']),
            pformat(resp),
        )
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
