from dashmips.mips import mips_instruction, Syscalls


def parse(arg):
    return tuple()


@mips_instruction('', parse)
def nop(regs, lbls):
    return True


@mips_instruction('', parse)
def syscall(regs, lbls):
    return Syscalls[regs['$v0']](regs, lbls, [])
