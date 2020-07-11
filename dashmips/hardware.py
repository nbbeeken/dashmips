"""Mips Hardware."""
from typing import Any, Dict, NoReturn, Tuple, Union, cast

from mypy_extensions import TypedDict
from typing_extensions import Literal

from .utils import as_twos_comp, intify

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
            raise Exception(f"Unknown register Reg[{key}]={hex(value)}")
        if value > 0xFFFF_FFFF:
            raise Exception(f"Registers are only 32-bits Reg[{key}]={hex(value)}")
        super().__setitem__(Registers.resolve[key], value & 0xFFFF_FFFF)

    def __getitem__(self, key: str) -> int:
        """Get register value."""
        if key in Registers.SPECIAL:
            return super().__getitem__(key)
        return as_twos_comp(super().__getitem__(Registers.resolve[key]))


SectionNames = Union[Literal["stack"], Literal["heap"], Literal["data"]]


class RAMPART(TypedDict):
    """Section of memory."""

    m: bytearray
    start: int
    stops: int


class RAM(TypedDict):
    """Structure of memory."""

    stack: RAMPART
    heap: RAMPART
    data: RAMPART


class Memory:
    """Memory simulated."""

    PAGE_SIZE = 2 ** 12
    TASK_LIMIT = 0xC0000000
    START_DATA = 0x00804900
    STACK_STOP = 0x05F5E100
    HEAP_START = 0x00600000

    def __init__(self):
        """Create Mips Memory."""
        self.ram: RAM = {
            "stack": {"m": bytearray(), "start": Memory.STACK_STOP, "stops": Memory.STACK_STOP},
            "heap": {"m": bytearray(), "start": Memory.HEAP_START, "stops": Memory.HEAP_START},
            "data": {"m": bytearray(), "start": Memory.START_DATA, "stops": Memory.START_DATA},
        }

    def _tlb(self, virtual_address: int, sizeof=1) -> Tuple[SectionNames, slice]:
        def v2p(pa: int):
            return slice(pa, pa + sizeof, 1)

        for section_name in self.ram:
            section_name = cast(SectionNames, section_name)
            start = self.ram[section_name]["start"]
            stops = self.ram[section_name]["stops"]

            if section_name == "stack" and start >= virtual_address >= stops:
                return section_name, v2p(start - virtual_address)

            if section_name == "stack" and virtual_address >= stops + Memory.PAGE_SIZE:
                # Auto growing stack, only grows if access is within a page
                self.ram["stack"]["m"].extend(bytearray(Memory.PAGE_SIZE))
                self.ram["stack"]["stops"] = self.ram["stack"]["start"] - len(self.ram["stack"]["m"])
                return section_name, v2p(start - virtual_address)

            if start <= virtual_address <= stops:
                return section_name, v2p(virtual_address - start)

        self._raise_index_error(virtual_address)

    def _raise_index_error(self, key: Any, address=None) -> NoReturn:
        ranges = " ".join([f"{sn}:[0x{s['start']:08x}, 0x{s['stops']:08x})" for sn, s in self.ram.items()])  # type: ignore
        tlb_msg = ""
        if address:
            tlb_msg = f" ; tlb generated {address}"
        if type(key) is slice:
            key_str = f"(0x{key.start:08x}, 0x{key.stop:08x})"
        else:
            key_str = f"0x{key:08x}"
        print(f"Error: {key_str} not in ranges {ranges}{tlb_msg}")
        exit(1)

    def extend_data(self, data: bytes, align_data=False) -> int:
        """Insert data into memory in data section."""
        section = self.ram["data"]

        if align_data:
            section["m"].extend(alignment_zeros(len(section["m"])))
            section["stops"] = section["start"] + len(section["m"])

        section["m"].extend(data)
        section["stops"] = section["start"] + len(section["m"])

        return section["stops"] - len(data)

    def extend_heap(self, data: bytes, align_data=False) -> int:
        """Insert data into memory in heap section."""
        section = self.ram["heap"]

        if align_data:
            section["m"].extend(alignment_zeros(len(section["m"])))
            section["stops"] = section["start"] + len(section["m"])

        section["m"].extend(data)
        section["stops"] = section["start"] + len(section["m"])

        return section["stops"] - len(data)

    def extend_stack(self, data: bytes, align_data=False) -> int:
        """Insert data into memory in stack section."""
        section = self.ram["stack"]

        if align_data:
            section["m"].extend(alignment_zeros(len(section["m"])))
            section["stops"] = section["start"] - len(section["m"])

        section["m"].extend(data[::-1])
        section["stops"] = section["start"] - len(section["m"])

        return section["stops"]

    def write08(self, virtual_address: int, values: bytes) -> None:
        """Store to memory."""
        section_name, physical_address = self._tlb(virtual_address, sizeof=1)
        if section_name == "stack":
            self.ram[section_name]["m"][physical_address] = values[::-1]
        else:
            self.ram[section_name]["m"][physical_address] = values

    def write16(self, virtual_address: int, values: bytes) -> None:
        """Store to memory."""
        section_name, physical_address = self._tlb(virtual_address, sizeof=2)
        if section_name == "stack":
            self.ram[section_name]["m"][physical_address] = values[::-1]
        else:
            self.ram[section_name]["m"][physical_address] = values

    def write32(self, virtual_address: int, values: bytes) -> None:
        """Store to memory."""
        section_name, physical_address = self._tlb(virtual_address, sizeof=4)
        if section_name == "stack":
            self.ram[section_name]["m"][physical_address] = values[::-1]
        else:
            self.ram[section_name]["m"][physical_address] = values

    def read08(self, virtual_address: int) -> bytes:
        """Search for and get item from ram section."""
        section_name, physical_address = self._tlb(virtual_address, sizeof=1)
        data = self.ram[section_name]["m"][physical_address]
        if section_name == "stack":
            return data[::-1]
        return data

    def read16(self, virtual_address: int) -> bytes:
        """Search for and get item from ram section."""
        section_name, physical_address = self._tlb(virtual_address, sizeof=2)
        data = self.ram[section_name]["m"][physical_address]
        if section_name == "stack":
            return data[::-1]
        return data

    def read32(self, virtual_address: int) -> bytes:
        """Search for and get item from ram section."""
        section_name, physical_address = self._tlb(virtual_address, sizeof=4)
        data = self.ram[section_name]["m"][physical_address]
        if section_name == "stack":
            return data[::-1]
        return data

    def read_str(self, virtual_address: int) -> str:
        """Read null terminated string from memory."""
        bin_string = []
        offset = 0
        while True:
            byte = intify(self.read08(virtual_address + offset), unsigned=True)
            if byte == 0:
                # null terminator encountered
                break
            bin_string.append(byte)
            offset += 1
        return "".join([chr(c) for c in bin_string])

    def write_str(self, virtual_address: int, data: bytes):
        """Write data string to memory."""
        for offset, byte in enumerate(data):
            self.write08(virtual_address + offset, bytes(byte))


def alignment_zeros(data_len) -> bytearray:
    """Return array of 0s to align to 4."""
    alignment = (4 - data_len % 4) % 4
    return bytearray(alignment)
