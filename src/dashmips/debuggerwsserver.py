"""Debugger over websockets."""
import websockets
from websockets import WebSocketServerProtocol
import asyncio
import json
import logging as log
import functools

from typing import Any

from dashmips.models import MipsProgram
from dashmips.debugger import COMMANDS


async def dashmips_debugger(client: WebSocketServerProtocol, path: str):
    """Client handler for debug server."""
    log.info(f'client={client} path={path}')
    try:
        async for message in client:
            log.debug(f'Recv "{message}"')
            req = json.loads(message)
            ret = COMMANDS[req['method']](params=req['params'])
            res = json.dumps(ret)
            log.debug(f'Send "{res}"')
            await client.send(res)
    except websockets.ConnectionClosed:
        log.warn('Client disconnect')
    except Exception as e:
        log.error(f'Unknown error: {e}')
    finally:
        log.warn('Debugging is truly over')
        # await client.close()
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
        level=log.DEBUG if should_log else log.CRITICAL,
    )
    logger = log.getLogger('websockets.server')
    logger.addHandler(log.StreamHandler())

    log.info(f'Starting server: ws://{host}:{port}')

    for name, command in COMMANDS.items():
        COMMANDS[name] = functools.partial(command, program=program)

    start_server = websockets.serve(dashmips_debugger, host, port)
    try:
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt as e:
        log.warn('Debugger exiting')
    finally:
        asyncio.get_event_loop().close()
