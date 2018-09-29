"""Derective handling."""
from dashmips.hardware import Memory


def align(name: str, data: str, memory: Memory):
    """Align directive."""
    return None


def asciiz(name: str, data: str, memory: Memory):
    """Asciiz directive."""
    string = data[1:-1].encode('ascii', 'ignore').decode('unicode_escape')
    asciiz_bytes = (string + '\0').encode()
    address = memory.malloc(len(asciiz_bytes))
    memory[address] = asciiz_bytes
    return address


def ascii(name: str, data: str, memory: Memory):
    """Ascii directive."""
    string = data[1:-1].encode('ascii', 'ignore').decode('unicode_escape')
    ascii_bytes = (string).encode()
    address = memory.malloc(len(ascii_bytes))
    memory[address] = ascii_bytes
    return address


def byte(name: str, data: str, memory: Memory):
    """Byte directive."""
    return None


def double(name: str, data: str, memory: Memory):
    """Double directive."""
    return None


def end_macro(name: str, data: str, memory: Memory):
    """End_macro directive."""
    return None


def eqv(name: str, data: str, memory: Memory):
    """Eqv directive."""
    return None


def extern(name: str, data: str, memory: Memory):
    """Extern directive."""
    return None


def globl(name: str, data: str, memory: Memory):
    """Globl directive."""
    return None


def half(name: str, data: str, memory: Memory):
    """Half directive."""
    return None


def include(name: str, data: str, memory: Memory):
    """Include directive."""
    return None


def macro(name: str, data: str, memory: Memory):
    """Macro directive."""
    return None


def set(name: str, data: str, memory: Memory):
    """Set directive."""
    return None


def space(name: str, data: str, memory: Memory):
    """Space directive."""
    return None


def word(name: str, data: str, memory: Memory):
    """Word directive."""
    return None
