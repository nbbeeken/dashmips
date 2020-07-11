"""Utilities.

Functions that do not depend on anything in the project.
"""
from typing import Union, List


class MipsException(Exception):
    """Mips related errors."""

    def __init__(self, message: str):
        """Create MipsException."""
        super().__init__(message)
        self.message = message


def parse_int(int_str: str) -> int:
    """Take a python number literal and returns an int."""
    arg: Union[int, str] = eval(int_str)

    if isinstance(arg, str):
        arg = int(ord(arg))
    else:
        arg = int(arg)

    return arg


def hexdump(data: bytes, *, offset=0, reverse_idx=False) -> str:
    """Build a hexdump from a bytestring."""
    ROW_MUL = 4
    ROW_HAF = 2
    hex_string = ""
    rows = []
    row: List[int] = []
    for idx, byte in enumerate(data):
        if idx % ROW_MUL == 0:
            row = [] if idx != 0 else row
            rows.append(row)
        row.append(byte)

    for idx, byte_row in enumerate(rows):
        if reverse_idx:
            calc_idx = ((len(rows) - 1) * ROW_MUL) - (idx * ROW_MUL)
        else:
            calc_idx = idx * ROW_MUL
        calc_idx += offset
        hex_string += f"{calc_idx:08x}  "
        hex_string += " ".join([f"{byte:02x}" for byte in byte_row[:ROW_MUL]])
        hex_string += "  " if len(byte_row) > ROW_HAF else " "
        hex_string += " ".join([f"{byte:02x}" for byte in byte_row[ROW_MUL:]])
        spaces = "" if idx != len(rows) - 1 else " " * (ROW_MUL - len(byte_row)) * 3
        ascii_str = "".join([chr(byte) if ord(" ") <= byte <= ord("~") else "." for byte in byte_row])
        hex_string += f"{spaces}  |{ascii_str}|"
        hex_string += "\n"

    return hex_string


def intify(values: bytes, unsigned=False) -> int:
    """Convert bytes to int."""
    return int.from_bytes(values, byteorder="big", signed=(not unsigned))


def bytesify(data: Union[str, int, bytes], *, size=None, null_byte=True) -> bytes:
    """Take variety of types and turn them into bytes."""
    if isinstance(data, str):
        return bytes(data + ("\0" if null_byte else ""), "utf8")
    if isinstance(data, int):
        int_size = size if size else (data.bit_length() // 8) + 1
        return (data & 0xFFFF_FFFF).to_bytes(int_size, "big")
    return bytes(data)


def as_twos_comp(value: int) -> int:
    """Interpret number as 32-bit twos comp value."""
    if value & 0x8000_0000 != 0:
        # negative
        flipped_value = (~value) & 0xFFFF_FFFF
        return -(flipped_value + 1)
    else:
        # positive
        return value
