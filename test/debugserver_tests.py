"""Tests for Mips Debug Server."""
import unittest
from subprocess import Popen
from shlex import split
from socket import socket
import json
from time import sleep

SERVER = Popen(split("python -m dashmips -d test.mips"))
sleep(0.5)
SOCKET = socket()
SOCKET.connect(('localhost', 9999))
rfile = SOCKET.makefile('r', encoding='utf8', buffering=1)
wfile = SOCKET.makefile('w', encoding='utf8', buffering=1)


class TestMipsDebugServer(unittest.TestCase):
    """Testing for mips debug server."""

    def test_start(self):
        """Test start command."""
        wfile.write(json.dumps({'command': 'start', 'value': ''}) + '\r\n')
        wfile.flush()
        resp = json.loads(rfile.readline().strip())

        program = resp['value']

        self.assertIn('command', resp)
        self.assertIn('value', resp)
        self.assertEqual(resp['command'], 'start')
        self.assertEqual(
            program['labels']['main'][1],
            program['registers']['pc'],
        )
        self.assertLessEqual(
            program['registers']['pc'],
            len(program['code'])
        )
        self.stop_debugging()

    def stop_debugging(self):
        """Send a proper stop command to the debugger."""
        stop_cmd = json.dumps({'command': 'stop', 'value': ''})
        wfile.write(stop_cmd + '\r\n')
        wfile.flush()
        resp = json.loads(rfile.readline().strip())
        self.assertIn('command', resp)
        self.assertIn('value', resp)
        self.assertEqual(resp['command'], 'stop')
        self.assertEqual(resp['value'], 'end debug session')
        SERVER.kill()

if __name__ == '__main__':
    try:
        unittest.main()
    finally:
        SERVER.kill()
