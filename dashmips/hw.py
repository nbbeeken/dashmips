
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
    def __init__(self):
        super().__init__({
            i: 0 for i in range(0, 32)
        })

    def __setitem__(self, key, value):
        if type(key) is str:
            key = RegnameToRegNum[key]
        if key == 0:
            return 0
        return super().__setitem__(key, value)

    def __getitem__(self, key):
        if type(key) is str:
            key = RegnameToRegNum[key]
        return super().__getitem__(key)

    def update(self, d):
        remap = {RegnameToRegNum[k]: v for k, v in d.items()}
        return super().update(remap)


class MIPSMemory(list):
    pass


SyscallFunctions = {
    1: (lambda regs, memory: print(regs['$a0'])),
    4: (lambda regs, memory: print(memory[regs['$a0']])),
}
