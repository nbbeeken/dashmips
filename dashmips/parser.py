"""
MIPS Parser
"""
import ply.lex as lex
import ply.yacc as yacc

from dashmips.nodes import StringNode, RTypeInstructionNode, InstructionSetNode
from dashmips.mips import MIPSMnemonics, MIPSDirectives


class Parser:
    def __init__(self):
        self.lexer = lex.lex(module=self)
        self.parser = yacc.yacc(module=self)

    def parse(self, text):
        rootNode = yacc.parse(text)
        if rootNode:
            rootNode.execute()
        else:
            print("error in parsing, debug me plz")


class MIPSParser(Parser):

    labels = {}
    tokens = (
        "LPAREN",
        "RPAREN",
        "COMMA",
        "NEWLINE",
        "DATA_SEC",
        "TEXT_SEC",
        "INSTRUCTION",
        "STRING",
        "LABEL",
        "COLON",
        "DIRECTIVE",
        "REGISTER",
        "NUMBER",
    )

    t_ignore = " \t"
    t_ignore_COMMENT = r"\#.*"

    t_LPAREN = r"\("
    t_RPAREN = r"\)"
    t_COMMA = r","
    t_COLON = r":"
    t_NUMBER = r'\d+'
    t_DATA_SEC = r".data"
    t_TEXT_SEC = r".text"
    t_INSTRUCTION = "|".join(MIPSMnemonics)
    t_DIRECTIVE = "|".join([r'\.' + dirc for dirc in MIPSDirectives])
    t_REGISTER = r"hi|lo|(\$((t[0-9]|s[0-7]|v[0-1]|a[0-3])|zero|sp|fp|gp|ra))"

    nl_re = r"\n+"

    @lex.TOKEN(nl_re)
    def t_NEWLINE(self, t):
        self.lexer.lineno += len(t.value)
        return t

    string_re = r'"[^"\\\r\n]*(?:\\.[^"\\\r\n]*)*"'

    @lex.TOKEN(string_re)
    def t_STRING(self, t):
        t.value = StringNode(str(t.value[1 : len(str(t.value)) - 1]))
        return t

    label_re = r"[a-zA-Z_][a-zA-Z0-9_]*"

    @lex.TOKEN(label_re)
    def t_LABEL(self, t):
        if t.value not in MIPSDirectives and t.value not in MIPSMnemonics:
            return t

    def t_error(self, t):
        print(f"Illegal character {t.value}")
        t.lexer.skip(1)

    ####################################################

    def p_program(self, p):
        """program : TEXT_SEC NEWLINE lines
                   | DATA_SEC NEWLINE datas
                   | program"""
        print(f"program {p}")

    def p_datas(self, p):
        """datas : data NEWLINE datas
                 | data NEWLINE"""
        print(f"datas {p}")

    def p_data(self, p):
        """data : LABEL COLON DIRECTIVE STRING"""
        print(f"data {p}")

    def p_lines(self, p):
        """lines : line NEWLINE lines
                 | line NEWLINE"""
        print(f"lines {p}")

    def p_line(self, p):
        """line : INSTRUCTION REGISTER COMMA REGISTER COMMA REGISTER
                | INSTRUCTION REGISTER COMMA NUMBER
                | INSTRUCTION REGISTER COMMA LABEL"""
        print(f"line {p}")

    def p_error(self, p):
        if p:
            print(p)
            print(f"SYNTAX ERROR: {repr(p.value)} AT LINE {p.lineno} TYPE {p.type}")
