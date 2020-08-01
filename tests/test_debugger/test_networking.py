"""Tests for the socket server."""

from typing import Optional
from subprocess import PIPE, Popen, run
from shlex import split
import time
import pytest
import socket as net
import json

from dashmips.debuggerserver import send_dashmips_message, receive_dashmips_message

SHOULD_START_SERVER = True
ADDRESS = ("localhost", 2390)


@pytest.fixture()
def server():
    """Start dashmips server."""
    if SHOULD_START_SERVER:
        debugger = Popen(split("python -m dashmips debug -i localhost -l tests/test_mips/smallest.mips"))
        time.sleep(0.2)  # sleep so we can connect
        assert debugger.returncode is None, "dashmips exited before we could test"
        return debugger
    return None


def prepend_header(message: str) -> bytes:
    """Prepends dashmips protocol header."""
    return bytes(json.dumps({"size": len(bytes(message, "utf8"))}) + message, "utf8")


def test_connect(server):
    """Test that the socket is available for connecting."""
    if server:
        assert server.returncode is None, "Dashmips Exited before we could test!!"
    try:
        s = net.create_connection(ADDRESS)
        assert s is not None
    except ConnectionRefusedError as e:
        assert False, "Failed to connect"

    if server:
        server.kill()  # Avoid reuse addr errors
        time.sleep(0.2)  # sleep so we can reconnect


def test_handshake(server):
    """Test that the socket is available for connecting."""
    s = net.create_connection(ADDRESS)
    assert s is not None

    send_dashmips_message(s, '{"method": "start"}')
    response = receive_dashmips_message(s)

    assert "result" in response
    assert "pid" in response["result"]
    if server:
        assert server.pid == response["result"]["pid"]

    send_dashmips_message(s, json.dumps({"method": "stop"}))

    if server:
        server.kill()  # Avoid reuse addr errors
        time.sleep(0.2)  # sleep so we can reconnect
