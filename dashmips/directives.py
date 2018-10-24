"""Derective handling."""
from dashmips.hardware import Memory


def align(name: str, data: str, memory: Memory) -> None:
    """Align directive.

    :param name: str:
    :param data: str:
    :param memory: Memory:

    """
    return None


def asciiz(name: str, data: str, memory: Memory) -> int:
    """Asciiz directive.

    :param name: str:
    :param data: str:
    :param memory: Memory:

    """
    string = data[1:-1].encode('ascii', 'ignore').decode('unicode_escape')
    asciiz_bytes = (string + '\0').encode()
    address = memory.malloc(len(asciiz_bytes))
    memory[address:address + len(asciiz_bytes)] = asciiz_bytes
    return address


def _ascii(name: str, data: str, memory: Memory) -> int:
    """Ascii directive.

    :param name: str:
    :param data: str:
    :param memory: Memory:

    """
    string = data[1:-1].encode('ascii', 'ignore').decode('unicode_escape')
    ascii_bytes = (string).encode()
    address = memory.malloc(len(ascii_bytes))
    memory[address:address + len(ascii_bytes)] = ascii_bytes
    return address


def byte(name: str, data: str, memory: Memory) -> None:
    """Byte directive.

    :param name: str:
    :param data: str:
    :param memory: Memory:

    """
    return None


def half(name: str, data: str, memory: Memory) -> None:
    """Half directive.

    :param name: str:
    :param data: str:
    :param memory: Memory:

    """
    return None


def space(name: str, data: str, memory: Memory) -> None:
    """Space directive.

    :param name: str:
    :param data: str:
    :param memory: Memory:

    """
    return None


def word(name: str, data: str, memory: Memory) -> None:
    """Word directive.

    :param name: str:
    :param data: str:
    :param memory: Memory:

    """
    return None
