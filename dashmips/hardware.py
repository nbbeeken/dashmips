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
    """Memory simulated."""

    PAGE = 2**12
    TASK_LIMIT = 0xc0000000
    START_DATA = 0x08049000
    STACK_STOP = 0x00000400

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

    def _tlb(self, virtual_address, sizeof=1):
        def v2p(pa): return slice(pa, pa + sizeof, 1)

        for section_name in self.ram:
            start = self.ram[section_name]["start"]
            stops = self.ram[section_name]["stops"]

            if section_name == "stack" and start >= virtual_address >= stops:
                return section_name, v2p(start - virtual_address)

            if start <= virtual_address <= stops:
                return section_name, v2p(virtual_address - start)

        self._raise_index_error(virtual_address)

    def _raise_index_error(self, key, address=None):
        ranges = " ".join([f"{sn}:[0x{s['start']:08x}, 0x{s['stops']:08x})" for sn, s in self.ram.items()])
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
        """Insert data into memory."""
        section = self.ram["data"]

        if align_data:
            section["m"].extend(alignment_zeros(len(section["m"])))
            section["stops"] = section["start"] + len(section["m"])

        section["m"].extend(data)
        section["stops"] = section["start"] + len(section["m"])

        return section["stops"] - len(data)

    def extend_stack(self, data: bytes, align_data=False) -> int:
        """Put data on stack."""
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


def alignment_zeros(data_len) -> bytearray:
    """Return array of 0s to align to 4."""
    alignment = ((4 - data_len % 4) % 4)
    return bytearray(alignment)
