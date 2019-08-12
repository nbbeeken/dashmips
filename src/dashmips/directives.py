"""Directive handling."""
from typing import Union
from .hardware import malloc


def parse_int(int_str: str) -> int:
    """Take a python number literal and returns an int."""
    arg: Union[int, str] = eval(int_str)

    if isinstance(arg, str):
        arg = int(ord(arg))
    else:
        arg = int(arg)

    return arg


def directive_align(name: str, data: str, memory: bytearray):
    """Align directive.

    :param name: str:
    :param data: str:
    :param memory: bytearray:
    """
    return None


def directive_asciiz(name: str, data: str, memory: bytearray) -> int:
    """Asciiz directive.

    :param name: str:
    :param data: str:
    :param memory: bytearray:
    """
    string = data[1:-1].encode("ascii", "ignore").decode("unicode_escape")
    asciiz_bytes = (string + "\0").encode()
    address = malloc(memory, len(asciiz_bytes))
    memory[address: address + len(asciiz_bytes)] = asciiz_bytes
    return address


def directive_ascii(name: str, data: str, memory: bytearray) -> int:
    """Ascii directive.

    :param name: str:
    :param data: str:
    :param memory: bytearray:
    """
    string = data[1:-1].encode("ascii", "ignore").decode("unicode_escape")
    ascii_bytes = (string).encode()
    address = malloc(memory, len(ascii_bytes))
    memory[address: address + len(ascii_bytes)] = ascii_bytes
    return address


def directive_byte(name: str, data: str, memory: bytearray) -> int:
    """Byte directive.

    :param name: str:
    :param data: str:
    :param memory: bytearray:
    """
    value = parse_int(data)
    if value > 0xFF:
        raise Exception("You cannot store a value greater than 2^8")
    address = malloc(memory, 1)
    memory[address] = value
    return address


def directive_half(name: str, data: str, memory: bytearray) -> int:
    """Half directive.

    :param name: str:
    :param data: str:
    :param memory: bytearray:
    """
    value = parse_int(data)
    if value > 0xFFFF:
        raise Exception("You cannot store a value greater than 2^16")
    address = malloc(memory, 2)
    memory[address: address + 2] = value.to_bytes(2, "big")
    return address


def directive_space(name: str, data: str, memory: bytearray) -> int:
    """Space directive.

    :param name: str:
    :param data: str:
    :param memory: bytearray:
    """
    value = parse_int(data)
    if value > 0xFFFF_FFFF:
        raise Exception("Please use less memory...")
    address = malloc(memory, value)
    return address


def directive_word(name: str, data: str, memory: bytearray) -> int:
    """Word directive.

    :param name: str:
    :param data: str:
    :param memory: bytearray:
    """
    value = parse_int(data)
    if value > 0xFFFF_FFFF:
        raise Exception("You cannot store a value greater than 2^32")
    address = malloc(memory, 4)
    memory[address: address + 4] = value.to_bytes(4, "big")
    return address
