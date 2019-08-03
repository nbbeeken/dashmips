"""Debugger over websockets."""
import websockets
from websockets import WebSocketServerProtocol
import asyncio
import json
import logging as log

from typing import Any

from dashmips.models import MipsProgram
from dashmips.debugger import COMMANDS

from jsonrpc import JSONRPCResponseManager, dispatcher


class ByteArrayJSON(json.JSONEncoder):
    """Encode bytearray from hex string."""

    def default(self, obj: Any) -> Any:
        """Serialize bytearray to hex."""
        if isinstance(obj, bytearray):
            return obj.hex()
        return json.JSONEncoder.default(self, obj)

    @staticmethod
    def bytearray_decoder(dct: dict) -> dict:
        """Decode bytearray from hex string."""
        if 'memory' in dct:
            dct['memory'] = bytearray().fromhex(dct['memory'])
        return dct


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

    for command_name, command in COMMANDS.items():
        dispatcher.add_method(command, command_name)

    async def dashmips_debugger(
        client: WebSocketServerProtocol, path: str
    ) -> None:
        """Client handler for debug server."""
        log.info(f'client={client} path={path}')
        try:
            message: str
            async for message in client:
                log.debug(f'Recv "{message}"')
                debug_response = JSONRPCResponseManager.handle_request(
                    message, dispatcher
                )
                log.debug(f'Send "{debug_response}"')
                await client.send(debug_response.json)

        except websockets.ConnectionClosed:
            log.warn('Client disconnect')
        except Exception as e:
            log.error(f'Unknown error: {e}')
        finally:
            log.warn('Debugging is truly over')
            return

    start_server = websockets.serve(dashmips_debugger, host, port)
    try:
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt as e:
        log.warn('Debugger exiting')
    finally:
        asyncio.get_event_loop().close()
