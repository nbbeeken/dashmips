"""
MIPS Parser
"""
import ply.lex as lex
import ply.yacc as yacc

from dashmips.nodes import StringNode, RTypeInstructionNode, InstructionSetNode


class Parser:

    def __init__(self):
        self.lexer = lex.lex(module=self)
        self.parser = yacc.yacc(module=self)

    def parse(self, text):
        rootNode = yacc.parse(text)
        if rootNode:
            rootNode.execute()
        else:
            print('error in parsing, debug me plz')


class MIPSParser(Parser):

    instructions = {}
    tokens = ('LPAREN', 'RPAREN', 'COMMA', 'NEWLINE',
              'DATA_SEC', 'TEXT_SEC', 'INSTRUCTION', 'STRING')

    t_ignore = ' \t'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_DATA_SEC = r'.data'
    t_TEXT_SEC = r'.text'

    instruction_re = r'[a-z]{1,5}'

    @lex.TOKEN(instruction_re)
    def t_INSTRUCTION(self, t):
        t.value = RTypeInstructionNode(t.value, 0, 0)

    nl_re = r'\n+'

    @lex.TOKEN(nl_re)
    def t_NEWLINE(self, t):
        t.lexer.lineno += len(t.value)

    string_re = r'"[^"\\\r\n]*(?:\\.[^"\\\r\n]*)*"'

    @lex.TOKEN(string_re)
    def t_STRING(self, t):
        t.value = StringNode(str(t.value[1:len(str(t.value)) - 1]))
        return t

    def t_error(self, t):
        print(f"Illegal character {t.value[0]}")
        t.lexer.skip(1)

    ####################################################

    def p_program(self, p):
        """program : TEXT_SEC NEWLINE lines"""
        p[0] = InstructionSetNode(p[2])

    def p_lines(self, p):
        """lines : line NEWLINE lines
                 | line NEWLINE"""
        if len(p) == 4:
            p[0] = InstructionSetNode([p[1]] + p[3])
        elif len(p) == 3:
            p[0] = InstructionSetNode([p[1]])

    def p_line(self, p):
        """line : INSTRUCTION"""
        p[0] = RTypeInstructionNode(p[0], 0, 0)

    def p_error(self, p):
        if p:
            print(f"SYNTAX ERROR: {p.value} AT LINE {p.lineno} TYPE {p.type}")
