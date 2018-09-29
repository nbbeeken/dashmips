"""Mips Debug Server."""
import json
import os
import sys
from dataclasses import dataclass, field, asdict
from socket import SOL_SOCKET, SO_REUSEADDR
from socketserver import TCPServer, StreamRequestHandler
from typing import List, Optional

from dashmips.preprocessor import MipsProgram

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


@dataclass
class DebugMessage:
    """Format for debug messages."""

    command: str
    program: MipsProgram
    breakpoints: List[int] = field(default_factory=list)
    message: str = ''
    error: bool = False

    def dumps(self):
        """Dump Json formatted Debug message"""
        msg = asdict(self)
        return json.dumps(msg)

    @staticmethod
    def loads(string):
        """Deserialize from json to DebugMessage."""
        from dashmips.debugger import Commands
        try:
            payload = json.loads(string)

            if ('command' not in payload and
                    payload['command'] not in Commands):
                # Json doesn't contain a valid command nor program
                return None

            if 'program' in payload:
                payload['program'] = MipsProgram(
                    **MipsProgram.from_dict(payload.get('program', {}))
                )
            else:
                payload['program'] = None  # command stop doesn't need a program
            return DebugMessage(**payload)
        except json.JSONDecodeError:
            return None


class MipsDebugRequestHandler(StreamRequestHandler):
    """Mips Debug Client Request Handler."""

    def respond(self, msg: DebugMessage):
        """Send response."""
        msg_to_send = msg.dumps().encode('utf8')
        self.wfile.write(msg_to_send + b'\r\n\r\n')
        self.wfile.flush()

    def receive(self) -> Optional[DebugMessage]:
        """Receive Client Command."""
        return DebugMessage.loads(self.rfile.readline().strip())

    def handle(self):
        """Handle Client Req."""
        from dashmips.debugger import Commands
        try:

            msg = self.receive()
            if msg is None:
                self.respond(BAD_MSG)
                return  # End this party now
            self.respond(Commands[msg.command](msg))

        except Exception as ex:
            # In case of any issues attempt to let client down easy
            # Exceptions only occur in errors of this program
            # they should not occur b/c of any bad input
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            err_msg = DebugMessage(**{
                'command': 'stop',
                'message': f'{fname}:{exc_tb.tb_lineno} {exc_type} {ex}',
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
                 server_address=('localhost', 9999),
                 RequestHandlerClass=MipsDebugRequestHandler,
                 bind_and_activate=True) -> None:
        """Create Mips Debug Server."""
        super().__init__(
            server_address,
            RequestHandlerClass,
            bind_and_activate
        )

    def server_bind(self):
        """Set reusable address opt."""
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)


def debug_mips(host='localhost', port=9999):
    """Create a debugging instance of mips."""
    with MipsDebugServer(server_address=(host, port)) as server:
        try:
            server.allow_reuse_address = True
            server.serve_forever()
        except KeyboardInterrupt:
            server.shutdown()
            server.server_close()
