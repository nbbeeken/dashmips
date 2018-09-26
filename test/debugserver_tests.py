"""Tests for Mips Debug Server."""
import unittest
from subprocess import Popen
from shlex import split
from socket import socket
import json
from time import sleep
from pprint import pformat

SERVER = Popen(split("python -m dashmips -d test.mips"))
sleep(0.1)  # Should be plenty of time to start and bind
SOCKET = socket()
SOCKET.connect(('localhost', 9999))
rfile = SOCKET.makefile('r', encoding='utf8', buffering=1)
wfile = SOCKET.makefile('w', encoding='utf8', buffering=1)


def send(msg):
    """Send json encoded message."""
    wfile.write(json.dumps(msg) + '\r\n')
    wfile.flush()


def recv():
    """Recv json encoded message."""
    resp = json.loads(rfile.readline().strip())
    return resp


class TestMipsDebugServer(unittest.TestCase):
    """Testing for mips debug server."""

    def test_start(self):
        """Test start command."""
        send({'command': 'start'})
        resp = recv()

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
            len(program['code']),
            pformat(resp),
        )
        self.stop_debugging()

    def stop_debugging(self):
        """Send a proper stop command to the debugger."""
        send({'command': 'stop'})
        resp = recv()
        self.assertIn('command', resp, pformat(resp))
        self.assertIn('program', resp, pformat(resp))
        self.assertIn('message', resp, pformat(resp))
        self.assertIn('error', resp, pformat(resp))
        self.assertEqual(resp['command'], 'stop', pformat(resp))
        self.assertEqual(resp['message'], 'end debug session', pformat(resp))
        SERVER.kill()

if __name__ == '__main__':
    try:
        unittest.main()
    finally:
        pass
        SERVER.kill()
