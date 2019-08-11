"""Mips Hardware."""
from typing import Dict, Optional, Union

names_enum = tuple(
    enumerate(
        (
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
            "pc",
            "hi",
            "lo",
            # fmt: on
        )
    )
)


class Registers(Dict[str, int]):
    """Mips Register File."""

    Resolve: Dict[Union[str, int], str] = {
        # **{i: name for (i, name) in names_enum},
        **{name: name for (i, name) in names_enum},
        **{f"${i}": name for (i, name) in names_enum},
    }

    def __init__(self, dictionary: Optional[Dict[str, int]] = None) -> None:
        """Initialize 32 registers to zero.

        dictionary - can be partial/full dictionary of registers
        """
        self.pc_changed = False
        base_reg = {name: 0 for idx, name in names_enum}
        if dictionary:
            new_dict = {
                Registers.Resolve[regname]: value
                for regname, value in dict(dictionary).items()
            }
            super().__init__({**base_reg, **new_dict})
        else:
            super().__init__(base_reg)

    def __setitem__(self, key: str, value: int) -> None:
        """
        Set register value.

        Accepts string or number for key
        """
        assert not value & 0x00_00_00_00, "Reg value cannot exceed 32 bits"
        self.pc_changed = Registers.Resolve[key] == "pc"
        super().__setitem__(Registers.Resolve[key], value)

    def __getitem__(self, key: str) -> int:
        """
        Get register value.

        Accepts string or number for key
        """
        return super().__getitem__(Registers.Resolve[key])


PAGE = 4096
FREESPACE = 0x0


def new_memory(hexstring: Optional[str] = None) -> bytearray:
    """Create 2KB of MIPS RAM."""
    global FREESPACE
    FREESPACE = 0x0
    memory = bytearray()
    if hexstring and type(hexstring) is str:
        memory.fromhex(hexstring)
    else:
        memory = bytearray(PAGE * 4)

    for i in range(0x2060, 0x2060 + ((80 * 25) * 2), 2):
        blank_space = (0x0F00 | ord(" "))
        memory[i:i + 1] = blank_space.to_bytes(2, 'little')

    return memory


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


def malloc(memory: bytearray, size: int) -> int:
    """Get aligned address of unused memory.

    :param size: int:
    """
    global FREESPACE
    pad = FREESPACE % 4
    if pad > 0:
        FREESPACE = FREESPACE + (4 - pad)
    oldFREESPACE = FREESPACE  # Aligned to 4
    FREESPACE += size + pad  # Allocate Aligned amount
    return oldFREESPACE
