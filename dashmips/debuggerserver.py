"""Debugger over sockets."""
import functools
import importlib
import inspect
import json
import logging as log
import signal
import socketserver
from socket import socket
import re

from .utils import MipsException
from .models import MipsProgram


HEADER_REGEX = re.compile(r'{\s*"size"\s*:\s*\d+\s*}')


class ProgramExit(Exception):
    """Program exited normally."""

    pass


def receive_dashmips_message(client: socket) -> dict:
    r"""Receive a dashmips debugger message.

    Dashmips communicates in a modified JSON-RPC format.
    An example message looks like (in regex form):
    {"size": \d+}{"method": "\w+"}
    Two concatenated JSON objects, the first reporting the size of the second object.
    """
    message = client.recv(30).decode("utf8")  # { "size": 9007199254740991 } <- largest message with some padding

    if message == "":
        # Client is disconnected! maybe we should just exit?
        return {"method": "stop"}

    header_search = HEADER_REGEX.match(message)
    if header_search:
        header = header_search[0]
    else:
        raise MipsException(f"Header not included in message: {message}")

    msg_size = json.loads(header)["size"]  # must be valid json {size: \d+}
    command = message[len(header) :]

    remaining_bytes = msg_size - len(command)
    if remaining_bytes > 0:
        command += client.recv(remaining_bytes).decode("utf8")

    return json.loads(command)


def send_dashmips_message(client: socket, data: str):
    r"""Send a dashmips debugger message.

    Size is calculated from the utf8 encoding of data.
    """
    data_encoded = bytes(data, "utf8")
    size = len(data_encoded)
    size_header = bytes(json.dumps({"size": size}), "utf8")
    out_message = size_header + data_encoded
    client.sendall(out_message)


def run_method(request: dict, commands: dict):
    """Message loop handler."""
    log.info(f"Recv `{request}`")

    if "method" not in request:
        raise MipsException("Must specify 'method' in debug messages.")

    method = request["method"]
    params = request.get("params", [])

    if method not in commands:
        raise MipsException(f"Unsupported method '{method}'.")

    command = commands[method]
    result = command(params=params)

    response = json.dumps({"method": request["method"], "result": result})

    if request["method"] != "info":
        log.info(f"Send `{response}`")
    else:
        log.info("Send info response")

    if "exited" in result:
        # only check top level
        raise ProgramExit

    return response


def debug_mips(program: MipsProgram, host="localhost", port=2390, should_log=False):
    """Create a debugging instance of mips.

    :param program: The compiled mips program
    :param host:  (Default value = "localhost")
    :param port:  (Default value = 2390)
    :param should_log:  (Default value = False)
    """
    log.basicConfig(
        format="%(asctime)-15s %(levelname)-7s %(message)s", level=log.INFO if should_log else log.CRITICAL,
    )
    logger = log.getLogger("sockets.server")
    logger.addHandler(log.StreamHandler())
    log.info(f"Serving on: tcp://{host}:{port}")

    class DashmipsTCPServerHandler(socketserver.BaseRequestHandler):
        def setup(self):
            # Collect functions from debugger.py
            debugger_module = importlib.import_module(".debugger", "dashmips")
            funcs = inspect.getmembers(debugger_module, inspect.isfunction)
            self.commands = {}
            for name, command in funcs:
                self.commands[name.replace("debug_", "")] = functools.partial(command, program=program)

        def handle(self):
            # self.request is the TCP socket connected to the client
            client: socket = self.request

            while True:  # Enter the loop that will continuously chat with the debugger client
                command = receive_dashmips_message(client)

                log.info(f"{self.client_address[0]} wrote: {command}")

                try:
                    response = run_method(command, self.commands)
                except ProgramExit:
                    log.info("Program exited normally")
                    break

                send_dashmips_message(client, response)

    # Allows server to reuse address to prevent crash
    socketserver.TCPServer.allow_reuse_address = True

    with socketserver.TCPServer((host, port), DashmipsTCPServerHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.handle_request()


def connectPreprocessFailure(host: str = "localhost", port: int = 2390):
    """Connect to extension and fail due to preprocessing failure."""

    class TCPHandler(socketserver.BaseRequestHandler):
        def handle(self):
            for _ in range(2):
                command = receive_dashmips_message(self.request)

                if b"verify_breakpoints" in command:
                    send_dashmips_message(self.request, '{"method": "verify_breakpoints", "result": []}')
                else:
                    send_dashmips_message(self.request, '{"method": "start", "result": {"exited": true}}')
                    return

    # Allows server to reuse address to prevent crash
    socketserver.TCPServer.allow_reuse_address = True
    socketserver.TCPServer.timeout = 0.1

    with socketserver.TCPServer((host, port), TCPHandler) as server:
        # Activate the server; this will keep running until you

        server.handle_request()
