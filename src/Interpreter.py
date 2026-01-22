
import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *
import sys
import numpy as np
import operator as op

sys.setrecursionlimit(10000)

class Interpreter(object):

    def __init__(self):
        self.memory_stack = MemoryStack()
        self.op_dict = {
            "+": op.add,
            "-": op.sub,
            "/": op.truediv,
            "*": np.dot,
            ".+": op.add,
            ".-": op.sub,
            ".*": op.mul,
            "./": op.truediv,
            "==": op.eq,
            "!=": op.ne,
            "<=": op.le,
            ">=": op.ge,
            "<": op.lt,
            ">": op.gt
        }

    @on('node')
    def visit(self, node):
        pass

    @when(AST.BinExpr)
    def visit(self, node):
        r1 = self.visit(node.left)
        r2 = self.visit(node.right)
        return self.op_dict[node.op](r1, r2)

    @when(AST.Assignment)
    def visit(self, node):
        val = self.visit(node.expression)

        if isinstance(node.ident, AST.ID):
            name = node.ident.var_name

            if node.op == "=":
                if self.memory_stack.get(name) is not None:
                    self.memory_stack.set(name, val)
                else:
                    self.memory_stack.insert(name, val)
            else:
                old_val = self.memory_stack.get(name)
                oper = node.op[:-1] # "+=" -> "+"
                new_val = self.op_dict[oper](old_val, self.visit(node.expression))
                self.memory_stack.set(name, new_val)
        elif isinstance(node.ident, AST.IdElements):
            matrix = self.memory_stack.get(node.ident.ident.var_name)
            indices = tuple(self.visit(i) for i in node.ident.elements)

            if node.op == "=":
                matrix[indices] = val
            else:
                oper = node.op[:-1]
                old_val = matrix[indices]
                matrix[indices] = self.op_dict[oper](old_val, val)


    @when(AST.IdElements)
    def visit(self, node):
        matrix = self.memory_stack.get(node.ident.var_name)
        indices = tuple(self.visit(i) for i in node.elements)

        return matrix[indices]

    @when(AST.If)
    def visit(self, node):
        if self.visit(node.expression):
            self.visit(node.instructions1)
        elif node.instruction2:
            self.visit(node.instructions2)

    @when(AST.While)
    def visit(self, node):
        while self.visit(node.expression):
            try:
                self.visit(node.instruction)
            except BreakException:
                break
            except ContinueException:
                continue

    @when(AST.ControlStatement)
    def visit(self, node):
        if node.instr == "break":
            raise BreakException()
        elif node.instr == "continue":
            raise ContinueException()

    @when(AST.Num)
    def visit(self, node):
        return node.value

    @when(AST.Variable)
    def visit(self, node):
        return self.memory_stack.get(node.name)

    @when(AST.ID)
    def visit(self, node):
        return self.memory_stack.get(node.var_name)

    @when(AST.Vector)
    def visit(self, node):
        return np.array([self.visit(e) for e in node.elements])

    @when(AST.Function)
    def visit(self, node):
        n = self.visit(node.arguments)

        if node.func_name == "zeros":
            return np.zeros((n, n))
        elif node.func_name == "ones":
            return np.ones((n, n))
        elif node.func_name == "eye":
            return np.eye(n)

        # To się raczej nigdy nie wykona, ale IDE mi narzekało, że nie ma returna
        raise Exception(f"Interpreter error: Unknown function name {node.func_name}")
