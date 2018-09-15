from mips import Instruction


def parse(arg):
    return tuple()


@Instruction(r'noop', parse)
def nop(regs, lbls):
    return True


@Instruction(r'syscall', parse)
def syscall(regs, lbls):
    return SyscallFn[regs['$v0']](regs, {})
