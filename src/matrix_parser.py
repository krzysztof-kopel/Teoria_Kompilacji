from sly import Parser
from matrix_scanner import MatrixScanner

class MatrixParser(Parser):
    tokens = MatrixScanner.tokens

    debugfile = '..\\out\\parser.out'

    precedence = (
        ("nonassoc", "IFX"),
        ("nonassoc", "ELSE"),
        ("nonassoc", "<", ">", "EQ", "NOT_EQ", "LESS_EQ", "MORE_EQ"),
        ("left", "+", "-", "DOT_PLUS", "DOT_SUB"),
        ("left", "*", "/", "DOT_MUL", "DOT_DIV"),
        ("right", "MIN_UNI"),
        ("left", "'")
    )

    # Program

    @_('instructions_opt')
    def program(self, p):
        pass

    @_('instructions')
    def instructions_opt(self, p):
        pass

    @_('')
    def instructions_opt(self, p):
        pass

    @_('instructions instruction')
    def instructions(self, p):
        pass

    @_('instruction')
    def instructions(self, p):
        pass

    @_('"{" instructions "}"')
    def instruction(self, p):
        pass

    @_('ID "[" row "]"')
    def expression(self, p):
        pass

    @_('ID "=" expression ";"')
    def instruction(self, p):
        pass

    @_('ID PLUS_ASSIGN expression ";"',
       'ID SUB_ASSIGN expression ";"',
       'ID MUL_ASSIGN expression ";"',
       'ID DIV_ASSIGN expression ";"')
    def instruction(self, p):
        pass

    @_('ID "[" row "]" "=" expression ";"')
    def instruction(self, p):
        pass

    @_('PRINT row ";"')
    def instruction(self, p):
        pass

    @_('IF "(" expression ")" instruction %prec IFX')
    def instruction(self, p):
        pass

    @_('IF "(" expression ")" instruction ELSE instruction')
    def instruction(self, p):
        pass

    @_('WHILE "(" expression ")" instruction')
    def instruction(self, p):
        pass

    @_('FOR ID "=" expression ":" expression instruction')
    def instruction(self, p):
        pass

    @_('BREAK ";"', 'CONTINUE ";"')
    def instruction(self, p):
        pass

    @_('RETURN expression ";"')
    def instruction(self, p):
        pass





    @_('INT_NUM', 'FLOAT_NUM', 'ID')
    def expression(self, p):
        pass

    @_('"(" expression ")"')
    def expression(self, p):
        pass

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
        pass

    @_("expression \"'\"")
    def expression(self, p):
        pass

    @_('"-" expression %prec MIN_UNI')
    def expression(self, p):
        pass

    @_('STRING')
    def expression(self, p):
        pass

    # MATRICES AND VECTORS

    @_('"[" row "]"')
    def expression(self, p):
        pass

    @_('row "," expression')
    def row(self, p):
        pass

    @_('expression')
    def row(self, p):
        pass

    # Functions

    @_('ZEROS "(" expression ")"',
       'ONES "(" expression ")"',
       'EYE "(" expression ")"')
    def expression(self, p):
        pass


    def error(self, p):
        if p:
            print(f"Syntax error at line {p.lineno}, token={p.type}, value='{p.value}'")
        else:
            print("Syntax error at EOF")