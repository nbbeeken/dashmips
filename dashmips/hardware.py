"""Mips Hardware."""
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Mapping,
    Optional,
    Tuple,
    Union,
    cast,
)

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
        """Intializes 32 registers to zero.

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


class Memory(List[int]):
    """Mips Big Endiean RAM."""

    PAGE = 4096

    def __init__(self, listish: Optional[Iterable[Any]] = None) -> None:
        """Create 2KB of MIPS RAM."""
        self._freespace = 0x4
        # if isinstance(listish, bytes) or isinstance(listish, str):
        #     listish = list(a85decode(listish, foldspaces=True))
        if listish is None:
            listish = []
        else:
            listish = list(listish)
        remaining_size = (3 * Memory.PAGE) - len(listish)

        self.on_change_listeners: List[Callable[["Memory"], None]] = []

        super().__init__([*listish, *([0] * remaining_size)])

        for i in range(0x2060, 0x2060 + ((80 * 25) * 2), 2):
            self[i] = 0x0F
            self[i + 1] = ord(" ")

    def on_change(self, cb: Callable[["Memory"], None]) -> None:
        """Insert on_change listener."""
        self.on_change_listeners.append(cb)

    def __setitem__(
        self, key: Union[int, slice], value: Union[int, Iterable[int]]
    ) -> None:
        """Bounds checking on access."""
        if isinstance(key, slice) and isinstance(value, (list, tuple, bytes)):
            # Handle slice assignment
            for byte in value:
                assert not (byte & 0x00), f"0x{byte:X} is greater than a byte"

        elif isinstance(key, slice) and isinstance(value, str):
            for char in value:
                byte = ord(char)
                assert not (byte & 0x00), f"0x{byte:X} is greater than a byte"

        elif isinstance(key, int) and isinstance(value, int):
            # Handle single index assignment
            assert not (value & 0x00), f"0x{value:X} is greater than a byte"

        super().__setitem__(key, value)  # type: ignore

    def __repr__(self) -> str:
        """Compacted Memory string."""
        s = "["
        zero_ct = 0
        for v in self:
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

    def malloc(self, size: int) -> int:
        """Get aligned address of unused memory.

        :param size: int:
        """
        pad = self._freespace % 4
        if pad > 0:
            self._freespace = self._freespace + (4 - pad)
        old_freespace = self._freespace  # Aligned to 4
        self._freespace += size + pad  # Allocate Aligned amount
        return old_freespace
