"""Mips Debug Server."""
import json
import sys
import os
from typing import Any, List, Dict
from socketserver import TCPServer, StreamRequestHandler
from socket import SOL_SOCKET, SO_REUSEADDR
from dataclasses import dataclass

from dashmips.MipsProgram import MipsProgram
BAD_MSG = json.dumps({
    'command': 'stop',
    'message': 'malformed message',
    'program': None,
    'error': True
})
ERR_MSG = json.dumps({
    'command': 'stop',
    'message': '500 internal error',
    'program': None,
    'error': True,
})
BYE_MSG = json.dumps({
    'command': 'stop',
    'message': 'end debug session',
    'program': None,
    'error': False
})


@dataclass
class DebugMessage:
    """Format for debug messages."""

    command: str
    message: str
    program: MipsProgram
    breakpoints: List[int]
    error: bool = False

    @staticmethod
    def from_json(jsonstr):
        """Deserialize from json to DebugMessage."""
        from dashmips.debugger import Commands

        try:
            payload = json.loads(jsonstr)

            if 'command' not in payload:
                # Json doesn't contain all the necessary fields
                return None

            if payload['command'] not in Commands:
                return None

            return DebugMessage(
                command=payload['command'],
                message=payload.get('message', ''),
                program=MipsProgram.from_json(**payload.get('program', {})),
                error=payload.get('error', False),
                breakpoints=payload.get('breakpoints', []),
            )
        except json.JSONDecodeError:
            return None

    def __iter__(self):
        """Iterate Debug message."""
        return iter(asdict(self).items())


class MipsDebugRequestHandler(StreamRequestHandler):
    """Mips Debug Client Request Handler."""

    def respond(self, msg):
        """Send response."""
        msg_to_send = msg
        if type(msg) is str:
            msg_to_send = msg.encode('utf8')
        elif type(msg) is dict:
            msg_to_send = json.dumps(msg).encode('utf8')

        self.wfile.write(msg_to_send + b'\r\n')
        self.wfile.flush()

    def receive(self) -> DebugMessage:
        """Receive Client Command."""
        return DebugMessage.from_json(self.rfile.readline().strip())

    def handle(self):
        """Handle Client Req."""
        try:
            while True:
                msg = self.receive()
                if not msg:
                    self.respond(BAD_MSG)
                    return

                if msg.command == 'start':
                    msg.program = self.server.program

                from dashmips.debugger import Commands
                resp = Commands[msg.command](msg)

                if msg.command == 'stop':
                    self.respond(BYE_MSG)
                    self.server.shutdown()
                    self.server.server_close()
                    exit(0)

                self.respond(dict(resp))
        except Exception as ex:
            # Incase of any issues attemp to let client down easy
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            err_msg = json.dumps({
                'command': 'stop',
                'message': str(f'{fname}:{exc_tb.tb_lineno} {exc_type} {ex}'),
                'program': None,
                'error': True,
            })
            self.respond(err_msg)
            # Arbitrarily large bad exit code to signal it was serious
            self.server.shutdown()
            self.server.server_close()
            exit(24)


class MipsDebugServer(TCPServer):
    """Mips Debug Server."""

    def __init__(self,
                 program: MipsProgram,
                 sourcemap: Dict[int, int],
                 server_address=('localhost', 9999),
                 RequestHandlerClass=MipsDebugRequestHandler,
                 bind_and_activate=True) -> None:
        """Create Mips Debug Server."""
        self.program = program
        self.sourcemap = sourcemap
        return super().__init__(
            server_address,
            RequestHandlerClass,
            bind_and_activate
        )

    def server_bind(self):
        """Set reusable address opt."""
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)


def debug_mips(program: MipsProgram, sourcemap: Dict[int, int]):
    """Create a debugging instance of mips."""
    with MipsDebugServer(program, sourcemap) as server:
        try:
            server.allow_reuse_address = True
            server.serve_forever()
        except KeyboardInterrupt:
            server.shutdown()
            server.server_close()
