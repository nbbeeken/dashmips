"""Mips Hardware."""
from base64 import a85encode, a85decode
from typing import Dict, Union

names_enum = tuple(enumerate((
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
)))

RegisterResolve: Dict[Union[str, int], str] = {
    **{i: name for (i, name) in names_enum},
    **{name: name for (i, name) in names_enum},
    **{f"${i}": name for (i, name) in names_enum},
}


class Registers(dict):
    """Mips Register File."""

    def __init__(self, dictionary=None):
        """Intializes 32 registers to zero.

        dictionary - can be partial/full dictionary of registers
        """
        base_reg = {name: 0 for idx, name in names_enum}
        if dictionary:
            new_dict = {
                RegisterResolve[regname]: value
                for regname, value in dict(dictionary).items()
            }
            super().__init__({
                **base_reg,
                **new_dict
            })
        else:
            super().__init__(base_reg)

    def __setitem__(self, key, value: int):
        """
        Set register value.

        Accepts string or number for key
        """
        return super().__setitem__(RegisterResolve[key], value)

    def __getitem__(self, key):
        """
        Get register value.

        Accepts string or number for key
        """
        return super().__getitem__(RegisterResolve[key])

    def update(self, d, **kwargs):
        """Resolve register names before calling dict update."""
        d.update(kwargs)
        remap = {
            RegisterResolve[k]: v
            for k, v in d.items()
        }
        return super().update(remap)

    def readablenum_registers(self):
        """Return a dictionary of $regnum->val."""
        return None

    def computer_registers(self):
        """Return a dictionary of num->val."""
        return None


class Memory(list):
    """Mips RAM."""

    KIB = 1024

    def __init__(self, listish=None):
        """Create 2KB of MIPS RAM."""
        self._freespace = 0x4
        # if isinstance(listish, bytes) or isinstance(listish, str):
        #     listish = list(a85decode(listish, foldspaces=True))
        if listish is None:
            listish = []
        else:
            listish = list(listish)
        remaining_size = (2 * Memory.KIB) - len(listish)

        super().__init__([
            *listish,
            *([0] * remaining_size)
        ])

    def __setitem__(self, key, value):
        """Bounds checking on access."""
        if 0x0 == key <= 0x3:
            from dashmips.mips import MipsException
            raise MipsException('NULL-ish pointer')
        try:
            for idx, val in enumerate(value):
                # val &= 0xFF
                super().__setitem__(key + idx, val)
            return self[key]
        except TypeError:
            # value &= 0xFF
            return super().__setitem__(key, value)

    def __repr__(self):
        """Compacted Memory string."""
        s = '['
        zero_ct = 0
        for v in self:
            if v == 0:
                zero_ct += 1
            else:
                if zero_ct != 0:
                    s += f'<0 repeats {zero_ct} times>, '
                    zero_ct = 0
                s += str(v) + ', '
        if zero_ct != 0:
            s += f'<0 repeats {zero_ct} times>, '
        s += ']'
        return s

    def malloc(self, size: int) -> int:
        """Get address of unused memory."""
        old_freespace = self._freespace
        self._freespace += size
        return old_freespace

    # def encoded_str(self):
    #     """Base85 encoding of memory."""
    #     return a85encode(bytes(self), foldspaces=True).decode('utf8')
