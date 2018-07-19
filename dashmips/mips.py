
RTypeInstructionMnemonics = [
    # ALU
    "addu",
    "add",
    "subu",
    "sub",
    "and",
    "or",
    "xor",
    "nor",
    "sltu",
    "slt",
    # Shift
    "sllv",
    "sll",
    "srlv",
    "srl",
    "srav",
    "sra",
    # Multiplication
    "mfhi",
    "mflo",
    "mthi",
    "mtlo",
    "multu",
    "mult",
    "divu",
    "div",
    # Jumps
    "jr",
    "jalr",
]

ITypeInstructionMnemonics = [
    # Loads
    "lbu",
    "lb",
    "lhu",
    "lh",
    "lwl",
    "lwr",
    "lw",
    # Stores
    "sb",
    "sh",
    "swr",
    "swl",
    "sw",
    # ALU
    "addiu",
    "addi",
    "sltiu",
    "slti",
    "andi",
    "ori",
    "xori",
    "lui",
    # Branch
    "bltz",
    "bgez",
    "bltzal",
    "bgtzal",
    "beq",
    "bne",
    "blez",
    "bgtz",
]

JTypeInstructionMnemonics = ["jal", "j",]

MIPSMnemonics = [
    *RTypeInstructionMnemonics,
    *ITypeInstructionMnemonics,
    *JTypeInstructionMnemonics,
]

MIPSDirectives = [
    "align",
    "asciiz",
    "ascii",
    "byte",
    "double",
    "end_macro",
    "eqv",
    "extern",
    "float",
    "globl",
    "half",
    "include",
    "macro",
    "set",
    "space",
    "word",
    # "ktext",
    # "kdata",
    # "text",
    # "data",
]
