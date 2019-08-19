"""Mips Hardware."""
from typing import Dict, Optional, Union, Iterable
from typing_extensions import Literal
from mypy_extensions import TypedDict
from collections.abc import ByteString

Section = TypedDict("Section", {"m": bytearray, "start": int, "stop": int})
RAM = TypedDict("RAM", {"data": Section, "stack": Section, "bss": Section, "heap": Section})

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


class Memory():
    """Memory simulated by bytearray."""

    PAGE = 2**12
    TASK_LIMIT = 0xc0000000
    START_DATA = 0x08049000
    STACK_STOP = 0x007A1200

    def __init__(self):
        """Create Mips Memory."""
        self.ram: RAM = {
            "stack": {
                "m": bytearray(),
                "start": Memory.STACK_STOP,
                "stop": Memory.STACK_STOP
            },
            "heap": {
                "m": bytearray(),
                "start": 0,
                "stop": 0
            },
            "data": {
                "m": bytearray(),
                "start": Memory.START_DATA,
                "stop": Memory.START_DATA
            },
        }

    def allocate(self, size):
        """Allocates size bytes of space in the data section (preprocess time)."""
        pad = self.freespace % 4
        if pad > 0:
            self.freespace = self.freespace + (4 - pad)
        old_freespace = self.freespace  # Aligned to 4
        self.freespace += size + pad  # Allocate Aligned amount
        return old_freespace

    def _get_section_name(self, key):
        for section_name, section in self.ram.items():
            if type(key) is int:
                if section["start"] >= key >= section["stop"]:
                    return section_name
            if type(key) is slice:
                if section["start"] >= key.start and key.stop <= section["stop"]:
                    return section_name
        ranges = " ".join([f"{sn}:[0x{s['start']:08x}, 0x{s['stop']:08x})" for sn, s in self.ram.items()])
        raise IndexError(f"{key} not in ranges {ranges}")

    def extend_data(self, data: bytes) -> int:
        """Insert data into memory."""
        section = self.ram["data"]
        section["m"].extend(data)
        section["stop"] = section["start"] + len(section["m"])
        return section["stop"] - len(data)

    def extend_stack(self, data) -> int:
        """Put data on stack."""
        section = self.ram["stack"]
        section["m"].extend(data)
        section["stop"] = section["start"] - len(section["m"])
        return section["stop"]

    def __setitem__(self, key, values):
        """Store to memory."""
        data = bytesify(values)
        section_name = self._get_section_name(key)
        section = self.ram[section_name]
        section["m"][key] = data

    def __getitem__(self, key):
        """Search for and get item from ram section."""
        return self.ram[self._get_section_name(key)]["m"]


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


def compact_memory_string(memory: bytearray) -> str:
    """Compacted Memory string."""
    s = "["
    zero_ct = 0
    for v in memory:
        if v == 0:
            zero_ct += 1
        else:
            if zero_ct != 0:
                s += f"<0 repeats {zero_ct} times>, "
                zero_ct = 0
            s += str(v) + ", "
    if zero_ct != 0:
        s += f"<0 repeats {zero_ct} times>, "
    s += "]"
    return s
