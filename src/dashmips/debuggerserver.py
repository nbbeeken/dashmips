"""Debugger over websockets."""
import importlib
import inspect
import websockets
import asyncio
import json
import logging as log
import functools
from websockets import WebSocketServerProtocol

from .models import MipsProgram


async def dashmips_debugger(
    client: WebSocketServerProtocol, path: str, commands
):
    """Client handler for debug server.

    :param client: Websocket handler
    :param path: should never be set '/'
    :param commands: dictionary of debug commands to functions
    """
    log.info(f'client={client.local_address}')
    try:
        async for message in client:
            log.info(f'Recv "{message}"')
            req = json.loads(message)
            ret = commands[req['method']](params=req['params'])
            res = json.dumps({'result': ret})
            log.info(f'Send "{res if req["method"] != "info" else ""}"')
            await client.send(res)

            if 'exited' in ret:
                # only check top level
                log.warn('Program exited')
                break

        await client.close()
    except websockets.ConnectionClosed:
        log.warning('Client disconnect')
    except Exception as e:
        log.error(f'Unknown error: {e}')


def debug_mips(
    program: MipsProgram,
    host: str = "localhost", port: int = 2390, should_log: bool = False
) -> None:
    """Create a debugging instance of mips.

    :param program: The compiled mips program
    :param host:  (Default value = 'localhost')
    :param port:  (Default value = 2390)
    :param should_log:  (Default value = False)
    """
    log.basicConfig(
        format="%(asctime)-15s %(levelname)-7s %(message)s",
        level=log.INFO if should_log else log.CRITICAL,
    )
    logger = log.getLogger('websockets.server')
    logger.addHandler(log.StreamHandler())
    log.info(f'Serving on: ws://{host}:{port}')

    # Collect functions from debugger.py
    debugger_module = importlib.import_module('.debugger', 'dashmips')
    funcs = inspect.getmembers(debugger_module, inspect.isfunction)
    commands = {}
    for name, command in funcs:
        commands[name.replace("debug_", "")] = functools.partial(
            command, program=program
        )

    # Bind commands positional arg before launching
    ws_func = functools.partial(dashmips_debugger, commands=commands)
    start_server = websockets.serve(ws_func, host, port)
    try:
        loop = asyncio.get_event_loop()
        ws_server = loop.run_until_complete(start_server)
        loop.run_forever()
    except KeyboardInterrupt as e:
        log.warning('bye bye... Debugger exiting...')
    finally:
        ws_server.close()
        loop.run_until_complete(ws_server.wait_closed())
        loop.close()
