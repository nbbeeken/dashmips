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
            i: 0 for i in range(0, 36)
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

    def pretty_str(self):
        """Generate Pretty String of Reg Contents."""
        return f"""$zero: {self[0]},
            $at: {self[1]},

            $v0: {self[2]}, $v1: {self[3]},

            $a0: {self[4]}, $a1: {self[5]}, $a2: {self[6]}, $a3: {self[7]},

            $t0: {self[8]}, $t1: {self[9]}, $t2: {self[10]}, $t3: {self[11]},
            $t4: {self[12]}, $t5: {self[13]}, $t6: {self[14]}, $t7: {self[15]},

            $s0: {self[16]}, $s1: {self[17]}, $s2: {self[18]}, $s3: {self[19]},
            $s4: {self[20]}, $s5: {self[21]}, $s6: {self[22]}, $s7: {self[23]},

            $t8: {self[24]}, $t9: {self[25]},

            $k0: {self[26]}, $k1: {self[27]},

            $gp: {self[28]}, $sp: {self[29]}, $fp: {self[30]}, $ra: {self[31]},

            pc: {self[32]},
            hi: {self[33]},
            lo: {self[34]},
        """


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
