"""Mips Debug Server."""
import json
from typing import Any
from socketserver import TCPServer, StreamRequestHandler
from dataclasses import dataclass, is_dataclass, asdict

from dashmips.MipsProgram import MipsProgram
BAD_MSG = json.dumps({'command': 'stop', 'value': 'malformed message'})
ERR_MSG = json.dumps({'command': 'stop', 'value': '500 internal eror'})
BYE_MSG = json.dumps({'command': 'stop', 'value': 'end debug session'})


@dataclass
class DebugMessage:
    """Format for debug messages."""

    command: str
    value: Any

    @staticmethod
    def from_json(jsonstr):
        """Deserialize from json to DebugMessage."""
        from dashmips.debugger import Commands

        try:
            jsonpayload = json.loads(jsonstr)

            if 'value' not in jsonpayload or 'command' not in jsonpayload:
                return None
            if jsonpayload['command'] not in Commands:
                return None

            return DebugMessage(
                command=jsonpayload['command'],
                value=jsonpayload['value'],
            )
        except json.JSONDecodeError:
            return None

    def to_dict(self):
        """Debug Message."""
        return {
            'command': self.command,
            'value': self.value
        }


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

    def receive(self):
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

                from dashmips.debugger import Commands
                resp = Commands[msg.command](self.server.program, msg)
                if not resp:
                    self.respond(BYE_MSG)
                    return

                self.respond(resp.to_dict())
        finally:
            # Incase of any issues attemp to let client down easy
            self.respond(ERR_MSG)
            # Arbitrarily large bad exit code to signal it was serious
            exit(24)


class MipsDebugServer(TCPServer):
    """Mips Debug Server."""

    def __init__(self,
                 program: MipsProgram,
                 server_address=('localhost', 9999),
                 RequestHandlerClass=MipsDebugRequestHandler,
                 bind_and_activate=True) -> None:
        """Create Mips Debug Server."""
        self.program = program
        return super().__init__(
            server_address,
            RequestHandlerClass,
            bind_and_activate
        )


def debug_mips(program: MipsProgram):
    """Create a debugging instance of mips."""
    with MipsDebugServer(program) as server:
        try:
            server.allow_reuse_address = True
            server.serve_forever()
        except KeyboardInterrupt:
            server.shutdown()
