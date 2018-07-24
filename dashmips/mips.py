from typing import List, Dict, Any

MIPSDirectives = {
    # fmt: off
    ".align":     (lambda data: None),
    ".asciiz":    (lambda data: (data[1:-1] + '\0').encode()),
    ".ascii":     (lambda data: (data[1:-1]).encode()),
    ".byte":      (lambda data: None),
    ".double":    (lambda data: None),
    ".end_macro": (lambda data: None),
    ".eqv":       (lambda data: None),
    ".extern":    (lambda data: None),
    ".globl":     (lambda data: None),
    ".half":      (lambda data: None),
    ".include":   (lambda data: None),
    ".macro":     (lambda data: None),
    ".set":       (lambda data: None),
    ".space":     (lambda data: None),
    ".word":      (lambda data: None),
    # ".float",
    # ".ktext",
    # ".kdata",
    # ".text",
    # ".data",
    # fmt: on
}

######################################
# 3 Args
######################################

instr_rd_rs_rt = {
    'pattern': (r"{instr_gap}({register}){args_gap}({register})" +
                r"{args_gap}({register})"),
    'parse': (lambda arg: (arg[2], arg[3], arg[4])),
    # fmt: off
    'instructions': {
        "add":  (lambda regs, lbls, rd, rs, rt: None),
        "addu": (lambda regs, lbls, rd, rs, rt: None),  # TODO: Implement me
        "and":  (lambda regs, lbls, rd, rs, rt: None),  # TODO: Implement me
        "movn": (lambda regs, lbls, rd, rs, rt: None),  # TODO: Implement me
        "movz": (lambda regs, lbls, rd, rs, rt: None),  # TODO: Implement me
        "mul":  (lambda regs, lbls, rd, rs, rt: None),  # TODO: Implement me
        "nor":  (lambda regs, lbls, rd, rs, rt: None),  # TODO: Implement me
        "or":   (lambda regs, lbls, rd, rs, rt: None),  # TODO: Implement me
        "sllv": (lambda regs, lbls, rd, rs, rt: None),  # TODO: Implement me
        "slt":  (lambda regs, lbls, rd, rs, rt: None),  # TODO: Implement me
        "sltu": (lambda regs, lbls, rd, rs, rt: None),  # TODO: Implement me
        "srav": (lambda regs, lbls, rd, rs, rt: None),  # TODO: Implement me
        "srlv": (lambda regs, lbls, rd, rs, rt: None),  # TODO: Implement me
        "sub":  (lambda regs, lbls, rd, rs, rt: None),  # TODO: Implement me
        "subu": (lambda regs, lbls, rd, rs, rt: None),  # TODO: Implement me
        "xor":  (lambda regs, lbls, rd, rs, rt: None),  # TODO: Implement me
    }
    # fmt: on
}

instr_rs_rt_label = {
    'pattern': (r"{instr_gap}({register}){args_gap}({register})" +
                r"{args_gap}({label})"),
    'parse': (lambda arg: (arg[2], arg[3], str(arg[4]))),
    'instructions': {
        "beq": (lambda regs, lbls, rs, rt, label: None),
        "bne": (lambda regs, lbls, rs, rt, label: None),
    },
}

instr_rs_rt_number = {
    'pattern': (r"{instr_gap}({register}){args_gap}({register})" +
                r"{args_gap}({number})"),
    'parse': (lambda arg: (arg[2], arg[3], int(arg[4]))),
    # fmt: off
    'instructions': {
        "addi":  (lambda regs, lbls, rs, rt, num: regs.update({rs: rt+num})),
        "addiu": (lambda regs, lbls, rs, rt, num: None),
        "ori":   (lambda regs, lbls, rs, rt, num: None),
        "andi":  (lambda regs, lbls, rs, rt, num: None),
        "slti":  (lambda regs, lbls, rs, rt, num: None),
        "sltiu": (lambda regs, lbls, rs, rt, num: None),
        "xori":  (lambda regs, lbls, rs, rt, num: None),
        "sra":   (lambda regs, lbls, rs, rt, num: None),
        "sll":   (lambda regs, lbls, rs, rt, num: None),
        "srl":   (lambda regs, lbls, rs, rt, num: None),
    }
    # fmt: on
}

instr_rs_number_rt = {
    'pattern': r"{instr_gap}({register}){args_gap}({number}?)\(({register})\)",
    'parse': (lambda arg: (arg[2],  int(arg[3]), arg[4])),
    # fmt: off
    'instructions': {
        "lb":  (lambda regs, lbls, rs, num, rt: None),
        "lbu": (lambda regs, lbls, rs, num, rt: None),
        "lh":  (lambda regs, lbls, rs, num, rt: None),
        "lhu": (lambda regs, lbls, rs, num, rt: None),
        "lw":  (lambda regs, lbls, rs, num, rt: None),
        "lwl": (lambda regs, lbls, rs, num, rt: None),
        "sc":  (lambda regs, lbls, rs, num, rt: None),
        "lwr": (lambda regs, lbls, rs, num, rt: None),
        "sb":  (lambda regs, lbls, rs, num, rt: None),
        "sw":  (lambda regs, lbls, rs, num, rt: None),
        "swl": (lambda regs, lbls, rs, num, rt: None),
        "swr": (lambda regs, lbls, rs, num, rt: None),
        "sh":  (lambda regs, lbls, rs, num, rt: None),
    }
    # fmt: on
}

######################################
# 2 Args
######################################

instr_rs_label = {
    'pattern': r"{instr_gap}({register}){args_gap}({label})",
    'parse': (lambda arg: (arg[2], str(arg[3]))),
    # fmt: off
    'instructions': {
        "bgez":   (lambda regs, lbls, rs, label: None),
        "bgezal": (lambda regs, lbls, rs, label: None),
        "bgtz":   (lambda regs, lbls, rs, label: None),
        "blez":   (lambda regs, lbls, rs, label: None),
        "bltz":   (lambda regs, lbls, rs, label: None),
        "bltzal": (lambda regs, lbls, rs, label: None),
    }
    # fmt: on
}

instr_rs_rt = {
    'pattern': r"{instr_gap}({register}){args_gap}({register})",
    'parse': (lambda arg: (arg[2], arg[3])),
    # fmt: off
    'instructions': {
        "jalr":  (lambda regs, lbls, rs, rt: None),
        "madd":  (lambda regs, lbls, rs, rt: None),
        "maddu": (lambda regs, lbls, rs, rt: None),
        "msubu": (lambda regs, lbls, rs, rt: None),
        "msub":  (lambda regs, lbls, rs, rt: None),
        "multu": (lambda regs, lbls, rs, rt: None),
        "mult":  (lambda regs, lbls, rs, rt: None),
        "clo":   (lambda regs, lbls, rs, rt: None),
        "clz":   (lambda regs, lbls, rs, rt: None),
        "div":   (lambda regs, lbls, rs, rt: None),
        "divu":  (lambda regs, lbls, rs, rt: None),
    }
    # fmt: on
}

instr_rd_number = {
    'pattern': r"{instr_gap}({register}){args_gap}({number})",
    'parse': (lambda arg: (arg[2], int(arg[3]))),
    'instructions': {
        "lui": (lambda regs, lbls, rd, num: None),
    }
}

######################################
# 1 Arg
######################################

instr_rd = {
    'pattern': r"{instr_gap}({register})",
    'parse': (lambda arg: (arg[2],)),
    'instructions': {
        "mflo": (lambda regs, lbls, rd: None),
        "mfhi": (lambda regs, lbls, rd: None),
        "mthi": (lambda regs, lbls, rd: None),
        "mtlo": (lambda regs, lbls, rd: None),
    }
}

instr_rs = {
    'pattern': r"{instr_gap}({register})",
    'parse': (lambda arg: (arg[2],)),
    # fmt: off
    'instructions': {
        "jr":   (lambda regs, lbls, rs: None),
        # "jalr": (lambda regs, lbls, rs: None), # This is an exception
    }
    # fmt: on
}

instr_label = {
    'pattern': r"{instr_gap}({label})",
    'parse': (lambda arg: (str(arg[2]),)),
    # fmt: off
    'instructions': {
        "j":   (lambda regs, lbls, label: None),
        "jal": (lambda regs, lbls, label: None),
    }
    # fmt: on
}

######################################
# 0 Args
######################################

instr_special = {
    'pattern': '',
    'parse': (lambda arg: tuple()),
    'instructions': {
        "nop": (lambda regs, lbls: True),
        "syscall": (lambda regs, lbls: None),
    }
}

RE_REGISTER = (r"hi|lo|(?:\$(?:(?:t[0-9]|s[0-7]|v[0-1]|a[0-3])" +
               r"|zero|sp|fp|gp|ra))")
RE_LABEL = r"[a-zA-Z_][a-zA-Z0-9_]*"
RE_DIRECTIVE = "\\" + "|\\".join(MIPSDirectives.keys())

RE_INSTRGAP = r"\s+"
RE_ARGSGAP = r"\s*,\s*"

RE_DEC = "(?:(?:+|-)?)(?:(?:[1-9](?:_?[0-9])*)|(?:0(?:_?0)*))"
RE_BIN = "(?:0(?:b|B)(?:_?[0-1])+)"
RE_OCT = "(?:0(?:o|O)(?:_?[0-7])+)"
RE_HEX = "(?:0(?:x|X)(?:_?([0-9]|[a-f]|[A-F]))+)"

RE_NUMBERS = [
    RE_DEC,
    RE_BIN,
    RE_OCT,
    RE_HEX,
]

RE_NUMBER = "(?:\d+)"  # "(?:" + "|".join(RE_NUMBERS) + ")"

REGEXS = {
    'register': RE_REGISTER,
    'label': RE_LABEL,
    'number': RE_NUMBER,
    'instr_gap': RE_INSTRGAP,
    'args_gap': RE_ARGSGAP,
}


def instr_re(i, p): return f"({i}){p}".format(**REGEXS)


instructionsOfArgs: Dict[int, List[Dict[str, Any]]] = {
    0: [instr_special],
    1: [instr_rd, instr_rs, instr_label],
    2: [instr_rs_label, instr_rs_rt, instr_rd_number],
    3: [
        instr_rd_rs_rt, instr_rs_rt_label,
        instr_rs_rt_number, instr_rs_number_rt
    ]
}

INSTRUCTION_GROUPS: List[Dict[str, Any]] = sorted([
    {
        'args': 3,
        'instruction_regexs': [
            instr_re(instruction, instruction_group_list['pattern'])
            for instruction_group_list in instructionsOfArgs[3]
            for instruction in instruction_group_list['instructions'].keys()
        ],
        'instruction_fns': {
            instr: fn
            for ig in instructionsOfArgs[3]
            for instr, fn in ig['instructions'].items()
        },
        'instruction_parsers': {
            instr: ig['parse']
            for ig in instructionsOfArgs[3]
            for instr in ig['instructions'].keys()
        }
    },
    {
        'args': 2,
        'instruction_regexs': [
            instr_re(instruction, instruction_group_list['pattern'])
            for instruction_group_list in instructionsOfArgs[2]
            for instruction in instruction_group_list['instructions'].keys()
        ],
        'instruction_fns': {
            instr: fn
            for ig in instructionsOfArgs[2]
            for instr, fn in ig['instructions'].items()
        },
        'instruction_parsers': {
            instr: ig['parse']
            for ig in instructionsOfArgs[2]
            for instr in ig['instructions'].keys()
        }
    },
    {
        'args': 1,
        'instruction_regexs': [
            instr_re(instruction, instruction_group_list['pattern'])
            for instruction_group_list in instructionsOfArgs[1]
            for instruction in instruction_group_list['instructions'].keys()
        ],
        'instruction_fns': {
            instr: fn
            for ig in instructionsOfArgs[1]
            for instr, fn in ig['instructions'].items()
        },
        'instruction_parsers': {
            instr: ig['parse']
            for ig in instructionsOfArgs[1]
            for instr in ig['instructions'].keys()
        }
    },
    {
        'args': 0,
        'instruction_regexs': [
            instr_re(instruction, instruction_group_list['pattern'])
            for instruction_group_list in instructionsOfArgs[0]
            for instruction in instruction_group_list['instructions'].keys()
        ],
        'instruction_fns': {
            instr: fn
            for ig in instructionsOfArgs[0]
            for instr, fn in ig['instructions'].items()
        },
        'instruction_parsers': {
            instr: ig['parse']
            for ig in instructionsOfArgs[0]
            for instr in ig['instructions'].keys()
        },
    },
], key=lambda g: g['args'])


if __name__ == '__main__':
    from pprint import pprint as pretty
    pretty(INSTRUCTION_GROUPS)
