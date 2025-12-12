#!/usr/bin/python
import AST
from SymbolTable import SymbolTable, VariableSymbol

# TODO: make it work on opers.m
class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)


    def generic_visit(self, node):        # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        elif hasattr(node, "__dict__"):
            for value in node.__dict__.values():
                if isinstance(value, list):
                    for item in value:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(value, AST.Node):
                    self.visit(value)

    # simpler version of generic_visit, not so general
    #def generic_visit(self, node):
    #    for child in node.children:
    #        self.visit(child)



class TypeChecker(NodeVisitor):
    def __init__(self):
        self.table = SymbolTable(None, "global")
        self.loop_nesting = 0
        self.error_occurred = False

    def print_error(self, node, msg):
        self.error_occurred = True
        lineno = getattr(node, 'lineno', '?')
        print(f"Line {lineno}: {msg}")


    def visit_Instructions(self, node):
        for instruction in node.instructions:
            self.visit(instruction)

    def visit_BinExpr(self, node):
                                          # alternative usage,
                                          # requires definition of accept method in class Node
        res1 = self.visit(node.left)     # type1 = node.left.accept(self)
        res2 = self.visit(node.right)    # type2 = node.right.accept(self)
        op    = node.op

        if res1 is None or res2 is None:
            return None

        type1, size1 = res1 if isinstance(res1, tuple) else (res1, None)
        type2, size2 = res2 if isinstance(res2, tuple) else (res2, None)

        if type1 == "string" or type2 == "string":
            if type1 == "string" and type2 == "string" and op == "+":
                return "string"
            else:
                self.print_error(node, f"Cannot use operator {op} with strings")
                return None

        if type1 == "matrix" or type2 == "matrix":
            if type1 != type2:
                self.print_error(node, f"Incompatible types for '{op}': {type1} & {type2}")
                return None

            if size1 is not None and size2 is not None:
                if op in ["+", "-", ".+", ".-", ".*", "./"]:
                    if size1 != size2:
                        self.print_error(node, f"Matrix dimension mismatch: {size1} vs {size2}")
                        return None

            return "matrix", size1

        if type1 == "int" and type2 == "int":
            return "int"

        return "float"

    def visit_Num(self, node):
        if isinstance(node.value, int):
            return "int"
        return "float"

    def visit_String(self, node):
        return "string"

    def visit_Variable(self, node):
        definition = self.table.get(node.name)

        if definition is not None:
            if definition.element_type == "matrix":
                return "matrix", definition.size
            return definition.element_type

        self.print_error(node, f"Variable '{node.name}' not defined")
        return None

    def visit_Assignment(self, node):
        rhs_result = self.visit(node.expression)

        if rhs_result is None:
            return None

        size_rhs = None
        if isinstance(rhs_result, tuple):
            type_rhs, size_rhs = rhs_result
        else:
            type_rhs, rhs_size = rhs_result, None


        if node.op == "=":
            if isinstance(node.ident, AST.ID):
                var_name = node.ident.var_name
                self.table.put(var_name, VariableSymbol(var_name, type_rhs, size_rhs))

            elif isinstance(node.ident, AST.IdElements):
                type_lhs = self.visit(node.ident)

                if type_lhs and type_rhs == "matrix":
                    self.print_error(node, "Cannot assign matrix to a scalar element")

        else:
            if isinstance(node.ident, AST.ID):
                var_name = node.ident.var_name
                if not self.table.get(var_name):
                    self.print_error(node, f"Variable '{var_name}' not initialized")

            elif isinstance(node.ident, AST.IdElements):
                self.visit(node.ident)

        return type_rhs

    def visit_ID(self, node):
        symbol = self.table.get(node.var_name)

        if symbol:
            return symbol.element_type
        else:
            self.print_error(node, f"Variable '{node.var_name}' not defined")
            return None


    def visit_IdElements(self, node):
        matrix_name = node.ident

        if isinstance(node.ident, AST.ID):
            matrix_name = node.ident.var_name

        symbol = self.table.get(matrix_name)
        if not symbol:
            self.print_error(node, f"Matrix '{matrix_name}' not defined")
            return None

        if symbol.element_type != "matrix":
            self.print_error(node, f"Variable '{matrix_name}' is not a matrix")
            return None

        if len(node.elements) > 2:
            self.print_error(node, f"Matrix reference has too many indices ({len(node.elements)}), max 2 allowed")


        if node.elements:
            for idx in node.elements:
                idx_type = self.visit(idx)
                if idx_type != "int":
                    self.print_error(node, f"Matrix index must be an integer, got {idx_type}")

        return "int" # Zakładam, że macierze są wypełnione intami
    
    def visit_Vector(self, node):
        length = None
        for vector_element in node.elements:
            element_type = self.visit(vector_element)
            if element_type == "vector":
                if length is None:
                    length = len(vector_element.elements)
                elif len(vector_element.elements) != length:
                    self.print_error(node, f"Matrix has rows of different sizes")
                    return None
        return "vector"

    def visit_Function(self, node):
        arg_type = self.visit(node.arguments)

        size_val = None
        if isinstance(node.arguments, AST.Num):
            size_val = node.arguments.value

        if arg_type == "int":
            return "matrix", (size_val, size_val)
        else:
            self.print_error(node, f"Function argument has type '{arg_type}', should have int")
            return None

    def visit_While(self, node):
        self.loop_nesting += 1

        self.visit(node.expression)
        self.visit(node.instruction)

        self.loop_nesting -= 1

    def visit_For(self, node):
        self.table = self.table.pushScope("loop")
        self.loop_nesting += 1

        self.table.put(node.iterator.name, VariableSymbol(node.iterator.name, 'int'))

        self.visit(node.range_start)
        self.visit(node.range_end)
        self.visit(node.content)

        self.loop_nesting -= 1
        self.table = self.table.popScope()

    def visit_ControlStatement(self, node):
        if self.loop_nesting == 0:
            self.print_error(node, f"Instruction '{node.instr}' found outside loop")

    def visit_Return(self, node):
        if node.expression is not None:
            self.visit(node.expression)
