#!/usr/bin/python
import AST
from SymbolTable import SymbolTable, VariableSymbol


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)


    def generic_visit(self, node):        # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)

    # simpler version of generic_visit, not so general
    #def generic_visit(self, node):
    #    for child in node.children:
    #        self.visit(child)



class TypeChecker(NodeVisitor):
    def __init__(self):
        self.table = SymbolTable(None, "global")
        self.loop_nesting = 0

    def print_error(self, node, msg):
        lineno = getattr(node, 'lineno', '?')
        print(f"Line {lineno}: {msg}")

    def visit_BinExpr(self, node):
                                          # alternative usage,
                                          # requires definition of accept method in class Node
        type1 = self.visit(node.left)     # type1 = node.left.accept(self) 
        type2 = self.visit(node.right)    # type2 = node.right.accept(self)
        op    = node.op

        if type1 is None or type2 is None:
            return None

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

            return "matrix"

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
            return definition.type

        self.print_error(node, f"Variable '{node.name}' not defined")
        return None

    def visit_Assignment(self, node):
        type_rhs = self.visit(node.expression)

        if type_rhs is None:
            return None

        if node.op == "=":
            if isinstance(node.ident, AST.ID):
                var_name = node.ident.var_name
                self.table.put(var_name, VariableSymbol(var_name, type_rhs))

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
            return symbol.type
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
        if arg_type == "int":
            return "matrix"
        else:
            self.print_error(node, f"Function argument has type '{arg_type}', should have int")
            return None
