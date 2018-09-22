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


class Registers(dict):
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
        s = (f"$at: {self[1]:02},\n$v0: {self[2]:02}, " +
             f"$v1: {self[3]:02},\n$a0: {self[4]:02}, $a1: {self[5]:02}, " +
             f"$a2: {self[6]:02}, $a3: {self[7]:02},\n$t0: {self[8]:02}, " +
             f"$t1: {self[9]:02}, $t2: {self[10]:02}, $t3: {self[11]:02},\n" +
             f"$t4: {self[12]:02}, $t5: {self[13]:02}, $t6: {self[14]:02}, " +
             f"$t7: {self[15]:02},\n$s0: {self[16]:02}, $s1: {self[17]:02}, " +
             f"$s2: {self[18]:02}, $s3: {self[19]:02},\n$s4: {self[20]:02}, " +
             f"$s5: {self[21]:02}, $s6: {self[22]:02}, $s7: {self[23]:02},\n" +
             f"$t8: {self[24]:02}, $t9: {self[25]:02},\n$k0: {self[26]:02}, " +
             f"$k1: {self[27]:02},\n$gp: {self[28]:02}, $sp: {self[29]:02}, " +
             f"$fp: {self[30]:02}, $ra: {self[31]:02},\n pc: {self[32]:02},\n" +
             f" hi: {self[33]:02},\n lo: {self[34]:02},")
        return s


class Memory(list):
    """Mips RAM."""

    KIB = 1024

    def __init__(self):
        """Create 2KB of MIPS RAM."""
        super().__init__([0] * (2 * Memory.KIB))
        self._freespace = 0x4

    def __setitem__(self, key, value):
        """Bounds checking on access."""
        if 0x0 == key <= 0x3:
            raise Exception('NULL-ish pointer')
        try:
            for idx, val in enumerate(value):
                # val &= 0xFF
                super().__setitem__(key + idx, val)
            return self[key]
        except TypeError:
            # value &= 0xFF
            return super().__setitem__(key, value)

    def __repr__(self):
        """Compated Memory string."""
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
