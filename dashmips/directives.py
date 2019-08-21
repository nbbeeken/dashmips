"""Directive handling."""

from .hardware import Memory
from .utils import parse_int, bytesify, MipsException


def directive_align(data: str, memory: Memory):
    """Align directive."""
    raise MipsException("Unsupported directive.")
    return None


def directive_asciiz(data: str, memory: Memory) -> int:
    """Asciiz directive."""
    string = data[1:-1].encode("ascii", "ignore").decode("unicode_escape")
    address = memory.extend_data(bytesify(string, null_byte=True))
    return address


def directive_ascii(data: str, memory: Memory) -> int:
    """Ascii directive."""
    string = data[1:-1].encode("ascii", "ignore").decode("unicode_escape")
    address = memory.extend_data(bytesify(string, null_byte=False))
    return address


def directive_byte(data: str, memory: Memory) -> int:
    """Byte directive."""
    value = bytesify(parse_int(data), size=1)
    address = memory.extend_data(value)
    return address


def directive_half(data: str, memory: Memory) -> int:
    """Half directive."""
    value = bytesify(parse_int(data), size=2)
    address = memory.extend_data(value)
    return address


def directive_word(data: str, memory: Memory) -> int:
    """Word directive."""
    value = bytesify(parse_int(data), size=4)
    address = memory.extend_data(value)
    return address


def directive_space(data: str, memory: Memory) -> int:
    """Space directive."""
    value = parse_int(data)
    if value > 0x77359400:
        # 2 Gigabytes of space...
        raise MipsException("Please use less memory...")
    address = memory.extend_data(bytes([0] * value))
    return address
