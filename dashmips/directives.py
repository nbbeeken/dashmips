"""Directive handling."""
from typing import Union

from .hardware import Memory, bytesify


def parse_int(int_str: str) -> int:
    """Take a python number literal and returns an int."""
    arg: Union[int, str] = eval(int_str)

    if isinstance(arg, str):
        arg = int(ord(arg))
    else:
        arg = int(arg)

    return arg


def directive_align(data: str, memory: Memory):
    """Align directive.

    :param name: str:
    :param data: str:
    :param memory: Memory:
    """
    raise Exception("Unsupported directive.")
    return None


def directive_asciiz(data: str, memory: Memory) -> int:
    """Asciiz directive.

    :param name: str:
    :param data: str:
    :param memory: Memory:
    """
    string = data[1:-1].encode("ascii", "ignore").decode("unicode_escape")
    address = memory.extend_data(bytesify(string, null_byte=True))
    return address


def directive_ascii(data: str, memory: Memory) -> int:
    """Ascii directive.

    :param name: str:
    :param data: str:
    :param memory: Memory:
    """
    string = data[1:-1].encode("ascii", "ignore").decode("unicode_escape")
    address = memory.extend_data(bytesify(string, null_byte=False))
    return address


def directive_byte(data: str, memory: Memory) -> int:
    """Byte directive.

    :param name: str:
    :param data: str:
    :param memory: Memory:
    """
    value = bytesify(parse_int(data), size=1)
    address = memory.extend_data(value)
    return address


def directive_half(data: str, memory: Memory) -> int:
    """Half directive.

    :param name: str:
    :param data: str:
    :param memory: Memory:
    """
    value = bytesify(parse_int(data), size=2)
    address = memory.extend_data(value)
    return address


def directive_word(data: str, memory: Memory) -> int:
    """Word directive.

    :param name: str:
    :param data: str:
    :param memory: Memory:
    """
    value = bytesify(parse_int(data), size=4)
    address = memory.extend_data(value)
    return address


def directive_space(data: str, memory: Memory) -> int:
    """Space directive.

    :param name: str:
    :param data: str:
    :param memory: Memory:
    """
    value = parse_int(data)
    if value > 0x77359400:
        # 2 Gigabytes of space...
        raise Exception("Please use less memory...")
    address = memory.extend_data(bytes([0] * value))
    return address
