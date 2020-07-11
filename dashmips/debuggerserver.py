"""Debugger over sockets."""
import functools
import importlib
import inspect
import json
import logging as log
import signal
import socketserver

from .models import MipsProgram


class ProgramExit(Exception):
    """Program exited normally."""

    pass


def client_loop(message: str, commands: dict):
    """Message loop handler."""
    log.info(f"Recv `{message}`")

    request = json.loads(message)

    command = commands[request["method"]]
    result = command(params=request["params"])

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
            while True:
                header = b""
                while True:
                    header += self.request.recv(1)
                    if header and chr(header[-1]) == "}":
                        break
                    if len(header) >= 1000:
                        log.error("Communication error between client and server")
                        break

                msg_size = int(header[8:-1])
                command = self.request.recv(msg_size)

                log.info(f"{self.client_address[0]} wrote: {command}")

                try:
                    response = client_loop(command, self.commands)
                except ProgramExit:
                    log.info("Program exited normally")
                    break

                self.request.sendall(bytes(json.dumps({"size": len(response)}), "ascii") + bytes(response, "ascii"))

    # Allows server to reuse address to prevent crash
    socketserver.TCPServer.allow_reuse_address = True

    with socketserver.TCPServer((host, port), DashmipsTCPServerHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.handle_request()
