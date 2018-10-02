"""Mips Debug Server."""
import json
import os
import sys
from dataclasses import dataclass, field, asdict
from socket import SOL_SOCKET, SO_REUSEADDR
from socketserver import TCPServer, StreamRequestHandler
from typing import List, Optional

from dashmips.preprocessor import MipsProgram


@dataclass
class DebugMessage:
    """Format for debug messages."""

    command: str
    program: MipsProgram
    breakpoints: List[int] = field(default_factory=list)
    message: str = ''
    error: bool = False

    def __post_init__(self):
        """Ensure unique breakpoints."""
        # set to remove duplicates and sort
        self.breakpoints = sorted(set(self.breakpoints))

    def __iter__(self):
        """Make DebugMessage castable to dict."""
        return iter(asdict(self).items())

    @staticmethod
    def from_dict(payload: dict):
        """Deserialize from json to DebugMessage."""
        from dashmips.debugger import Commands

        if ('command' not in payload and
                payload['command'] not in Commands):
            # Json doesn't contain a valid command nor program
            return None

        if 'program' in payload:
            payload['program'] = MipsProgram.from_dict(
                payload.get('program', {})
            )
        else:
            payload['program'] = None
        return DebugMessage(**payload)


class MipsDebugRequestHandler(StreamRequestHandler):
    """Mips Debug Client Request Handler."""

    def respond(self, msg: DebugMessage):
        """Send response."""
        msg_to_send = json.dumps(dict(msg)).encode('utf8')
        self.wfile.write(msg_to_send + b'\r\n\r\n')
        self.wfile.flush()
        if self.server.log:
            print(f"{self.client_address}: Respond {msg}")

    def receive(self) -> Optional[DebugMessage]:
        """Receive Client Command."""
        try:
            msg = DebugMessage.from_dict(
                json.loads(self.rfile.readline().strip())
            )
            if self.server.log:
                print(f"{self.client_address}: Receive {msg}")
            return msg
        except json.JSONDecodeError:
            return None

    def handle(self):
        """Handle Client Req."""
        from dashmips.debugger import Commands
        try:
            if self.server.log:
                print(f"{self.client_address}: Connected")
            msg = self.receive()
            if msg is None:
                self.respond(DebugMessage(**{
                    'command': 'stop',
                    'message': 'malformed message',
                    'program': None,
                    'breakpoints': [],
                    'error': True,
                }))
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
            print(f'{fname}:{exc_tb.tb_lineno} {exc_type} {ex}')
            try:
                self.respond(err_msg)
            finally:
                # Arbitrarily large bad exit code to signal it was serious
                self.server.shutdown()
                self.server.server_close()
                exit(24)


class MipsDebugServer(TCPServer):
    """Mips Debug Server."""

    def __init__(self,
                 server_address=('0.0.0.0', 9999),
                 log=False,
                 RequestHandlerClass=MipsDebugRequestHandler,
                 bind_and_activate=True) -> None:
        """Create Mips Debug Server."""
        self.allow_reuse_address = True
        self.log = log
        super().__init__(
            server_address,
            RequestHandlerClass,
            bind_and_activate
        )
        if self.log:
            print(f"Server is listening on {self.socket.getsockname()}")

    def server_bind(self):
        """Set reusable address opt."""
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)


def debug_mips(host='localhost', port=9999, log=False):
    """Create a debugging instance of mips."""
    with MipsDebugServer(server_address=(host, port), log=log) as server:
        try:
            server.allow_reuse_address = True
            server.serve_forever()
        except KeyboardInterrupt:
            server.shutdown()
            server.server_close()
