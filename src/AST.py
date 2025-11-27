

class Node(object):
    pass

class Instructions(Node):
    def __init__(self, instructions):
        self.instructions = instructions

class Block(Node):
    def __init__(self, instructions):
        self.instructions = instructions

class Num(Node):
    def __init__(self, value):
        self.value = value

class Variable(Node):
    def __init__(self, name):
        self.name = name

class BinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class UnExpr(Node):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

class Assignment(Node):
    def __init__(self, op, ident, expression):
        self.op = op
        self.ident = ident
        self.expression = expression

class IdElements(Node):
    def __init__(self, ident, elements):
        self.ident = ident
        self.elements = elements

class Print(Node):
    def __init__(self, to_print):
        self.to_print = to_print

class If(Node):
    def __init__(self, expression, instruction1, instruction2=None):
        self.expression = expression
        self.instruction1 = instruction1
        self.instruction2 = instruction2

class While(Node):
    def __init__(self, expression, instruction):
        self.expression = expression
        self.instruction = instruction

class For(Node):
    def __init__(self, iterator, range_start, range_end, content):
        self.iterator = iterator
        self.range_start = range_start
        self.range_end = range_end
        self.content = content

class ControlStatement(Node):
    def __init__(self, instr):
        self.instr = instr

class Return(Node):
    def __init__(self, expression):
        self.expression = expression

class String(Node):
    def __init__(self, content):
        self.content = content

class Vector(Node):
    def __init__(self, elements):
        self.elements = elements

class Function(Node):
    def __init__(self, func_name, arguments):
        self.func_name = func_name
        self.arguments = arguments

# ...
# fill out missing classes
# ...

class Error(Node):
    def __init__(self):
        pass
      
