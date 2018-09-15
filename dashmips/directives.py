"""Derective handling master function."""


def align(data):
    """Align directive."""
    return None


def asciiz(data):
    """Asciiz directive."""
    return (data[1:-1] + '\0').encode()


def ascii(data):
    """Ascii directive."""
    return (data[1:-1]).encode()


def byte(data):
    """Byte directive."""
    return None


def double(data):
    """Double directive."""
    return None


def end_macro(data):
    """End_macro directive."""
    return None


def eqv(data):
    """Eqv directive."""
    return None


def extern(data):
    """Extern directive."""
    return None


def globl(data):
    """Globl directive."""
    return None


def half(data):
    """Half directive."""
    return None


def include(data):
    """Include directive."""
    return None


def macro(data):
    """Macro directive."""
    return None


def set(data):
    """Set directive."""
    return None


def space(data):
    """Space directive."""
    return None


def word(data):
    """Word directive."""
    return None
