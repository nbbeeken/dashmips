"""Debugger over websockets."""
import asyncio
import functools
import importlib
import inspect
import json
import logging as log

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

        response = json.dumps({"result": result})

        if request["method"] != "info":
            log.info(f"Send `{response}`")

        await client.send(response)

        if "exited" in result:
            # only check top level
            log.warn("Program exited")
            break


async def dashmips_debugger(client: WebSocketServerProtocol, path: str, commands: dict):
    """Client handler for debug server.

    :param client: Websocket handler
    :param path: should never be set always is `/`
    :param commands: dictionary of debug commands to functions
    """
    log.info(f"client={client.local_address}")
    try:
        client_loop(client, commands)
        await client.close()
    except websockets.ConnectionClosed:
        log.warning("Client disconnect")
    except Exception as e:
        log.error(f"Unknown error: {e}")


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

    # Bind commands positional arg before launching
    ws_func = functools.partial(dashmips_debugger, commands=commands)
    start_server = websockets.serve(ws_func, host, port)
    try:
        loop = asyncio.get_event_loop()
        ws_server = loop.run_until_complete(start_server)
        loop.run_forever()
    except KeyboardInterrupt as e:
        log.warning("bye bye... Debugger exiting...")
    finally:
        ws_server.close()
        loop.run_until_complete(ws_server.wait_closed())
        loop.close()
