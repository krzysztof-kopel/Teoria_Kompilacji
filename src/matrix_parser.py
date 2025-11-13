from sly import Parser
from matrix_scanner import MatrixScanner

class MatrixParser(Parser):
    tokens = MatrixScanner.tokens

    debugfile = 'parser.out'

    precedence = (
        ("nonassoc", "IFX"),
        ("nonassoc", "ELSE"),
        ("nonassoc", "<", ">", "EQ", "NOT_EQ", "LESS_EQ", "MORE_EQ"),
        ("left", "+", "-", "DOT_PLUS", "DOT_SUB"),
        ("left", "*", "/", "DOT_MUL", "DOT_DIV"),
        ("right", "MIN_UNI"),
        ("left", "'")
    )

    @_('INT_NUM', 'FLOAT_NUM', 'ID')
    def expression(self, p):
        return p[0]

    @_('"(" expression ")"')
    def expression(self, p):
        return p.expression

    @_('expression "+" expression',
       'expression "-" expression',
       'expression "*" expression',
       'expression "/" expression',
       'expression DOT_PLUS expression',
       'expression DOT_SUB expression',
       'expression DOT_MUL expression',
       'expression DOT_DIV expression',
       'expression EQ expression',
       'expression NOT_EQ expression',
       'expression LESS_EQ expression',
       'expression MORE_EQ expression',
       'expression "<" expression',
       'expression ">" expression')
    def expression(self, p):
        return p[1], p.expression0, p.expression1

    @_("expression \"'\"")
    def expression(self, p):
        return 'TRANSPOSE', p.expression

    @_('"-" expression %prec MIN_UNI')
    def expression(self, p):
        return 'UMINUS', p.expression

    @_('STRING')
    def expression(self, p):
        return p.STRING

    # MATRICES AND VECTORS

    @_('"[" rows "]"')
    def expression(self, p):
        return p.rows

    @_('"[" row "]"')
    def expression(self, p):
        return p.row

    @_('rows "," "[" row "]"')
    def rows(self, p):
        return p.rows + [p.row]

    @_('"[" row "]"')
    def rows(self, p):
        return [p.row]

    @_('row "," expression')
    def row(self, p):
        return p.row + [p.expression]

    @_('expression')
    def row(self, p):
        return [p.expression]

    # FUNCTIONS

    @_('ZEROS "(" expression ")"',
       'ONES "(" expression ")"',
       'EYE "(" expression ")"')
    def expression(self, p):
        return p[0], p.expression


    # Matrix element access

    @_('ID "[" row "]"')
    def expression(self, p):
        return 'REF', p.ID, p.row

    # Program

    @_('instructions_opt')
    def program(self, p):
        return p.instructions_opt

    @_('instructions')
    def instructions_opt(self, p):
        return p.instructions

    @_('')
    def instructions_opt(self, p):
        return []
