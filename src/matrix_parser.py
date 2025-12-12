from sly import Parser
from matrix_scanner import MatrixScanner
import AST, TreePrinter

class MatrixParser(Parser):
    def __init__(self):
        self.error_occurred = False
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
        return AST.Instructions(p.instructions_opt)

    @_('instructions')
    def instructions_opt(self, p):
        return p.instructions

    @_('')
    def instructions_opt(self, p):
        return []

    @_('instructions instruction')
    def instructions(self, p):
        return p.instructions + [p.instruction]

    @_('instruction')
    def instructions(self, p):
        return [p.instruction]

    @_('"{" instructions "}"')
    def instruction(self, p):
        return AST.Block(p.instructions)

    @_('ID "=" expression ";"')
    def instruction(self, p):
        node = AST.Assignment(p[1], AST.ID(p.ID), p.expression)
        node.lineno = p.lineno
        return node

    @_('ID PLUS_ASSIGN expression ";"',
       'ID SUB_ASSIGN expression ";"',
       'ID MUL_ASSIGN expression ";"',
       'ID DIV_ASSIGN expression ";"')
    def instruction(self, p):
        return AST.Assignment(p[1], AST.ID(p.ID), p.expression)

    @_('ID "[" row "]" "=" expression ";"')
    def instruction(self, p):
        return AST.Assignment(p[4], AST.ID(p.ID, p.row), p.expression)

    @_('PRINT row ";"')
    def instruction(self, p):
        return AST.Print(p.row)

    @_('IF "(" expression ")" instruction %prec IFX')
    def instruction(self, p):
        return AST.If(p.expression, p.instruction)

    @_('IF "(" expression ")" instruction ELSE instruction')
    def instruction(self, p):
        return AST.If(p.expression, p.instruction0, p.instruction1)

    @_('WHILE "(" expression ")" instruction')
    def instruction(self, p):
        return AST.While(p.expression, p.instruction)

    @_('FOR ID "=" expression ":" expression instruction')
    def instruction(self, p):
        return AST.For(AST.Variable(p.ID), p.expression0, p.expression1, p.instruction)

    @_('BREAK ";"', 'CONTINUE ";"')
    def instruction(self, p):
        node = AST.ControlStatement(p[0])
        node.lineno = p.lineno
        return node

    @_('RETURN expression ";"')
    def instruction(self, p):
        return AST.Return(p.expression)

    @_('ID "[" row "]"')
    def expression(self, p):
        return AST.ID(p.ID, p.row)

    @_('INT_NUM', 'FLOAT_NUM')
    def expression(self, p):
        return AST.Num(p[0])

    @_('ID')
    def expression(self, p):
        node = AST.Variable(p.ID)
        node.lineno = p.lineno
        return node

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
        node = AST.BinExpr(p[1], p.expression0, p.expression1)
        node.lineno = p.lineno
        return node

    @_("expression \"'\"")
    def expression(self, p):
        return AST.UnExpr("TRANSPOSE", p.expression)

    @_('"-" expression %prec MIN_UNI')
    def expression(self, p):
        return AST.UnExpr(p[0], p.expression)

    @_('STRING')
    def expression(self, p):
        return AST.String(p.STRING)

    # MATRICES AND VECTORS

    @_('"[" row "]"')
    def expression(self, p):
        node = AST.Vector(p.row)
        node.lineno = p.lineno
        return node

    @_('row "," expression')
    def row(self, p):
        return p.row + [p.expression]

    @_('expression')
    def row(self, p):
        return [p.expression]

    # Functions

    @_('ZEROS "(" expression ")"',
       'ONES "(" expression ")"',
       'EYE "(" expression ")"')
    def expression(self, p):
        return AST.Function(p[0], p.expression)


    def error(self, p):
        if p:
            self.error_occurred = True
            print(f"Syntax error at line {p.lineno}, token={p.type}, value='{p.value}'")
        else:
            print("Syntax error at EOF")