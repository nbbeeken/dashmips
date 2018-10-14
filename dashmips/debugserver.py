"""Mips Debug Server."""
import json
import os
import sys
import logging as log
from socket import socket, SOL_SOCKET, SO_REUSEADDR
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE
from typing import List, Optional, Tuple, TextIO

from dashmips.models import MipsProgram, DebugMessage, Client


class DebugServer:
    """DebugServer."""

    def __init__(self, address):
        """Create DebugServer."""
        self.clients: List[Client] = []

        self.listener = socket()
        self.listener.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.listener.setblocking(False)
        self.listener.bind(address)
        self.listener.listen(128)

        log.info(
            f'Listening on {self.listener.getsockname()}',
            extra={'client': ''}
        )

        self.sel = DefaultSelector()
        self.sel.register(self.listener, EVENT_READ)

    def shutdown(self):
        """Shutdown Server."""
        for c in self.clients:
            c.rfile.close()
            c.wfile.close()
        self.listener.close()
        self.sel.close()
        log.warning("Shutdown", extra={'client': ''})

    def find_client(self, fd):
        """Find client by rfile fd.

        :param fd:

        """
        for c in self.clients:
            if c.rfile.fileno() == fd:
                return c
        return None  # This cannot happen

    def run(self):
        """Run select loop."""
        while True:
            events = self.sel.select()
            for key, mask in events:
                if key.fd == self.listener.fileno():
                    self.accept()
                else:
                    client = self.find_client(key.fd)
                    self.handle(client)

    def accept(self):
        """Accept New Client."""
        client_socket, client_address = self.listener.accept()
        client_socket.setblocking(False)
        client = Client(
            client_socket.makefile('r', encoding='utf8'),
            client_socket.makefile('w', encoding='utf8'),
            client_address
        )
        self.clients.append(client)
        self.sel.register(client.rfile, EVENT_READ)
        log.debug('Added to clients', extra={'client': client.address})

    def handle(self, client: Client):
        """Handle Debug Request.

        :param client: who the incoming message is from

        """
        from dashmips.debugger import Commands

        log.debug('Handle', extra={'client': client.address})

        msg = self.receive(client)

        if msg is None:
            # Nothing to handle
            return

        self.respond(client, Commands[msg.command](msg))

    def respond(self, client: Client, msg: DebugMessage):
        """Send response.

        :param client: destination of response

        :param msg: message to send to client
        """
        msg_to_send = json.dumps(dict(msg))
        try:
            client.wfile.write(msg_to_send + '\n')
            client.wfile.flush()
            log.debug(
                f"Respond {msg.command}" +
                f"{(' - ' + msg.message) if msg.message else ''}",
                extra={'client': client.address}
            )
        except ConnectionError:
            log.error(
                'Could not respond to client',
                extra={'client': client.address}
            )
            self.remove_client(client)

    def receive(self, client: Client):
        """Receive Client Command.

        :param client: Client:

        """
        try:
            txt = client.rfile.readline().strip()

            if txt == '':
                # Client is closed.
                log.warning(
                    'Closed Connection', extra={'client': client.address}
                )
                self.remove_client(client)
                return None

            msg = DebugMessage.from_dict(json.loads(txt))
            log.debug(
                f"Receive {msg.command}" +
                f"{(' - ' + msg.message) if msg.message else ''}",
                extra={'client': client.address}
            )
            return msg
        except json.JSONDecodeError:
            log.error(
                'Could not decode JSON from client',
                extra={'client': client.address}
            )
            self.remove_client(client)
            return None
        except ConnectionError:
            log.error(
                'Could not receive from client',
                extra={'client': client.address}
            )
            self.remove_client(client)
            return None

    def remove_client(self, client):
        """Remove client from list.

        :param client:

        """
        self.clients.remove(client)
        try:
            self.sel.unregister(client.rfile)
            client.rfile.close()
            client.wfile.close()
            log.warning(
                'Removed from client list',
                extra={'client': client.address}
            )
        except (IOError, KeyError):
            log.warning(
                f'Failed to close down client',
                extra={'client': client.address}
            )


def debug_mips(host='localhost', port=9999, should_log=False):
    """Create a debugging instance of mips.

    :param host:  (Default value = 'localhost')
    :param port:  (Default value = 9999)
    :param should_log:  (Default value = False)

    """
    log.basicConfig(
        format='%(asctime)-15s %(levelname)-7s %(client)s: %(message)s',
        level=log.DEBUG if should_log else log.CRITICAL,
    )
    address = (host, port)
    server = DebugServer(address)
    try:
        server.run()
    except KeyboardInterrupt:
        server.shutdown()
