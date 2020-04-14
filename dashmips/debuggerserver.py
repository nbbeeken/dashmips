"""Debugger over websockets."""
import asyncio
import functools
import importlib
import inspect
import json
import logging as log
import signal

import websockets
from websockets import WebSocketServerProtocol

from .models import MipsProgram


async def client_loop(client: WebSocketServerProtocol, commands: dict):
    """Message loop handler."""
    async for message in client:
        log.info(f"Recv `{message}`")

        request = json.loads(message)

        command = commands[request["method"]]
        result = command(params=request["params"])

        response = json.dumps({"method": request["method"], "result": result})

        if request["method"] != "info":
            log.info(f"Send `{response}`")
        else:
            log.info("Send info response")

        await client.send(response)

        if "exited" in result:
            # only check top level
            log.error("Program exited")
            break


async def dashmips_debugger(client: WebSocketServerProtocol, path: str, commands: dict):
    """Client handler for debug server.

    :param client: Websocket handler
    :param path: should never be set always is `/`
    :param commands: dictionary of debug commands to functions
    """
    log.info(f"client={client.local_address}")
    try:
        await client_loop(client, commands)
        await client.close()
    except websockets.ConnectionClosed:
        log.error("Client disconnect")


def debug_mips(program: MipsProgram, host="localhost", port=2390, should_log=False):
    """Create a debugging instance of mips.

    :param program: The compiled mips program
    :param host:  (Default value = "localhost")
    :param port:  (Default value = 2390)
    :param should_log:  (Default value = False)
    """
    log.basicConfig(
        format="%(asctime)-15s %(levelname)-7s %(message)s",
        level=log.INFO if should_log else log.CRITICAL,
    )
    logger = log.getLogger("websockets.server")
    logger.addHandler(log.StreamHandler())
    log.info(f"Serving on: ws://{host}:{port}")

    # Collect functions from debugger.py
    debugger_module = importlib.import_module(".debugger", "dashmips")
    funcs = inspect.getmembers(debugger_module, inspect.isfunction)
    commands = {}
    for name, command in funcs:
        commands[name.replace("debug_", "")] = functools.partial(command, program=program)

    ws_func = functools.partial(dashmips_debugger, commands=commands)
    start_server = websockets.serve(ws_func, host, port, close_timeout=2000)
    loop = asyncio.get_event_loop()
    try:
        ws_server = asyncio.get_event_loop().run_until_complete(start_server)
        loop.run_forever()
    except KeyboardInterrupt:
        log.warning('Shutting down debugger...')
        loop.close()
