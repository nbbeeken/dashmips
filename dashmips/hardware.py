"""Mips Hardware."""
from typing import Dict, Union

register_names = (
    # fmt: off
    "$zero",
    "$at",
    "$v0", "$v1",
    "$a0", "$a1", "$a2", "$a3",
    "$t0", "$t1", "$t2", "$t3", "$t4", "$t5", "$t6", "$t7",
    "$s0", "$s1", "$s2", "$s3", "$s4", "$s5", "$s6", "$s7",
    "$t8", "$t9",
    "$k0", "$k1",
    "$gp", "$sp", "$fp", "$ra",
    # fmt: on
)


class Registers(Dict[str, int]):
    """Mips Register File."""

    SPECIAL = ("pc", "hi", "lo")

    resolve: Dict[Union[str, int], str] = {
        **{name: name for (i, name) in enumerate(register_names)},
        **{f"${i}": name for (i, name) in enumerate(register_names)},
    }

    def __init__(self):
        """Initialize 32 registers to zero.

        dictionary - can be partial/full dictionary of registers
        """
        for name in register_names:
            self[name] = 0x0

        # Special Registers
        self["pc"] = 0x0
        self["hi"] = 0x0
        self["lo"] = 0x0

    def __setitem__(self, key: str, value: int):
        """Set register value."""
        if key in Registers.SPECIAL:
            return super().__setitem__(key, value)
        if key not in Registers.resolve:
            raise Exception(f'Unknown register Reg[{key}]={hex(value)}')
        if value > 0xFFFFFFFF:
            raise Exception(f'Registers are only 32-bits Reg[{key}]={hex(value)}')
        super().__setitem__(Registers.resolve[key], value)

    def __getitem__(self, key: str) -> int:
        """Get register value."""
        if key in Registers.SPECIAL:
            return super().__getitem__(key)
        return super().__getitem__(Registers.resolve[key])


class Memory:
    """Memory simulated by bytearray."""

    PAGE = 2**12
    TASK_LIMIT = 0xc0000000
    START_DATA = 0x08049000
    STACK_STOP = 0x007A1200

    def __init__(self):
        """Create Mips Memory."""
        self.ram = {
            "stack": {
                "m": bytearray(),
                "start": Memory.STACK_STOP,
                "stops": Memory.STACK_STOP
            },
            "heap": {
                "m": bytearray(),
                "start": 0,
                "stops": 0
            },
            "data": {
                "m": bytearray(),
                "start": Memory.START_DATA,
                "stops": Memory.START_DATA
            },
        }

    def _tlb(self, key):
        for section_name in self.ram:
            start = self.ram[section_name]["start"]
            stops = self.ram[section_name]["stops"]

            if type(key) is int:
                if section_name == "stack" and start >= key >= stops:
                    return section_name, start - key

                if start <= key <= stops:
                    return section_name, key - start

            if type(key) is slice:
                if section_name == "stack" and start >= key.start and stops <= key.stop:
                    distance = abs(key.start - key.stop)
                    address_start = start - key.start
                    return "stack", slice(address_start, address_start + distance, key.step)

                if start <= key.start and stops >= key.stop:
                    distance = abs(key.start - key.stop)
                    address_start = key.start - stops
                    return section_name, slice(address_start, address_start + distance, key.step)

        self._raise_index_error(key)

    def _raise_index_error(self, key, address=None):
        ranges = " ".join([f"{sn}:[0x{s['start']:08x}, 0x{s['stops']:08x})" for sn, s in self.ram.items()])
        tlb_msg = ""
        if address:
            tlb_msg = f" ; tlb generated {address}"
        print(f"Error: 0x{key:08x} not in ranges {ranges}{tlb_msg}")
        exit(1)

    def extend_data(self, data: bytes) -> int:
        """Insert data into memory."""
        section = self.ram["data"]
        section["m"].extend(data)
        section["stops"] = section["start"] + len(section["m"])
        return section["stops"] - len(data)

    def extend_stack(self, data) -> int:
        """Put data on stack."""
        section = self.ram["stack"]
        section["m"].extend(data)
        section["stops"] = section["start"] - len(section["m"])
        return section["stops"] - len(data)

    def __setitem__(self, key, values):
        """Store to memory."""
        data = bytesify(values)
        section_name, address = self._tlb(key)
        try:
            self.ram[section_name]["m"][address] = data
        except IndexError:
            self._raise_index_error(key, address)

    def __getitem__(self, key):
        """Search for and get item from ram section."""
        section, address = self._tlb(key)
        try:
            return self.ram[section]["m"][address]
        except IndexError:
            self._raise_index_error(key, address)


def bytesify(data: Union[str, int, bytes], *, size=None, null_byte=True) -> bytes:
    """Take variety of types and turn them into bytes."""
    if isinstance(data, str):
        return bytes(data + ("\0" if null_byte else ""), "utf8")
    if isinstance(data, int):
        int_size = size if size else (data.bit_length() // 8) + 1
        return data.to_bytes(int_size, "big")
    return bytes(data)


def align(data: bytes) -> bytes:
    """Align bytes to multiple of 4 bytes."""
    alignment = len(data) + ((4 - len(data) % 4) % 4)
    return data + bytes(alignment)


def hexdump(data, *, offset=0, reverse_idx=False):
    """Build a hexdump from a bytestring."""
    hex_string = ""
    rows = []
    row = []
    for idx, byte in enumerate(data):
        if idx % 0x10 == 0:
            row = [] if idx != 0 else row
            rows.append(row)
        row.append(byte)

    for idx, byte_row in enumerate(rows):
        if reverse_idx:
            calc_idx = offset - (idx * 0x10)
        else:
            calc_idx = (idx * 0x10) + offset
        hex_string += f"{calc_idx:08x}  "
        hex_string += " ".join([f"{byte:02x}" for byte in byte_row[:8]])
        hex_string += "  " if len(byte_row) > 8 else ' '
        hex_string += " ".join([f"{byte:02x}" for byte in byte_row[8:]])
        spaces = '' if idx != len(rows) - 1 else ' ' * (16 - len(byte_row)) * 3
        ascii_str = "".join([
            chr(byte) if ord(' ') <= byte <= ord('~') else '.'
            for byte in byte_row
        ])
        hex_string += f"{spaces}  |{ascii_str}|"
        hex_string += "\n"

    return hex_string
