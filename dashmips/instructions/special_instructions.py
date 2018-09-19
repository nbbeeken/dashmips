from dashmips.mips import mips_instruction


def parse(arg):
    return tuple()


@mips_instruction(r'noop', parse)
def nop(regs, lbls):
    return True


@mips_instruction(r'syscall', parse)
def syscall(regs, lbls):
    return SyscallFn[regs['$v0']](regs, {})
