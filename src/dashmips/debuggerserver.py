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
    """Client handler for debug server."""
    log.info(f'client={client} path={path}')
    try:
        async for message in client:
            log.info(f'Recv "{message}"')
            req = json.loads(message)
            res = json.dumps(commands[req['method']](params=req['params']))
            log.info(f'Send "{res}"')
            await client.send(res)
            if 'exited' in res:
                break
        await client.close()
    except websockets.ConnectionClosed:
        log.warn('Client disconnect')
    except Exception as e:
        log.error(f'Unknown error: {e}')
    finally:
        log.warn('Debugging is truly over')
        # asyncio.get_running_loop().stop()
        return


def debug_mips(
    program: MipsProgram,
    host: str = "localhost", port: int = 2390, should_log: bool = False
) -> None:
    """Create a debugging instance of mips.

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
        log.warn('bye bye... Debugger exiting...')
    finally:
        ws_server.close()
        loop.run_until_complete(ws_server.wait_closed())
        loop.close()
