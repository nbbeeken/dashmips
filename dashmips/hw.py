"""Mips Hardware."""

MIPSRegisterNames = [
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
]

regplainname_to_regnum = {
    name: num for num, name in enumerate(MIPSRegisterNames)
}
regnumname_to_regnum = {
    f'${num}': num for num, name in enumerate(MIPSRegisterNames)
}
regnum_to_regnum = {
    num: num for num, _ in enumerate(MIPSRegisterNames)
}
RegnameToRegNum = {**regplainname_to_regnum, **regnumname_to_regnum}


class MIPSRegisters(dict):
    """Mips Register File."""

    def __init__(self):
        """Intializes 32 registers to zero."""
        super().__init__({
            i: 0 for i in range(0, 32)
        })

    def __setitem__(self, key, value):
        """
        Set register value.

        Accepts string or number for key
        """
        if type(key) is str:
            key = RegnameToRegNum[key]
        if key == 0:
            return 0
        return super().__setitem__(key, value)

    def __getitem__(self, key):
        """
        Get register value.

        Accepts string or number for key
        """
        if type(key) is str:
            key = RegnameToRegNum[key]
        return super().__getitem__(key)

    def update(self, d):
        """Resolve register names before calling dict update."""
        remap = {RegnameToRegNum[k]: v for k, v in d.items()}
        return super().update(remap)


class MIPSMemory(list):
    """Mips RAM."""

    KIB = 1024

    def __init__(self):
        """Create 2KB of MIPS RAM."""
        return super().__init__([0] * (2 * MIPSMemory.KIB))

    def __setitem__(self, key, value):
        """Bounds checking on access."""
        value &= 0xFF
        if 0x0 <= key <= 0x3:
            raise Exception('NULL-ish pointer')
        return super().__setitem__(key, value)


SyscallFn = {
    1: (lambda regs, memory: print(regs['$a0'])),
    4: (lambda regs, memory: print(memory.get(regs['$a0'], -1))),
    **{i: (lambda _, __: None) for i in range(5, 100)}
}
