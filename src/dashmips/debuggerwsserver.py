"""Debugger over websockets."""
import websockets
from websockets import WebSocketServerProtocol
import asyncio
import json
import logging as log

from dashmips.models import MipsProgram


def debug(debug_command: dict) -> dict:
    """Brains of the operation."""
    return {'operation': 'successful'}


async def dashmips_debugger(
    client: WebSocketServerProtocol, path: str
) -> None:
    """Client handler for debug server."""
    log.info(f'client={client} path={path}')
    try:
        async for message in client:
            debug_command = json.loads(message)
            log.debug(f'Recv "{debug_command}"')
            debug_response = debug(debug_command)
            log.debug(f'Send "{debug_response}"')
            await client.send(json.dumps(debug_response))
            break
    except websockets.ConnectionClosed:
        log.warn('Client disconnect')
    finally:
        log.warn('Debugging is truly over')


def debug_mips(
    program: MipsProgram,
    host: str = "localhost", port: int = 9999, should_log: bool = False
) -> None:
    """Create a debugging instance of mips.

    :param host:  (Default value = 'localhost')
    :param port:  (Default value = 9999)
    :param should_log:  (Default value = False)
    """
    log.basicConfig(
        format="%(asctime)-15s %(levelname)-7s %(message)s",
        level=log.DEBUG if should_log else log.CRITICAL,
    )
    logger = log.getLogger('websockets.server')
    # logger.setLevel(log.ERROR)
    logger.addHandler(log.StreamHandler())

    log.info('Starting server!')

    start_server = websockets.serve(dashmips_debugger, host, port)
    try:
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt as e:
        log.warn('Debugger exiting')
    finally:
        asyncio.get_event_loop().close()
