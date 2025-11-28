import AST

def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator

class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @staticmethod
    def print_indent_prefix(indent):
        print("|  " * indent, end="")

    @addToClass(AST.Instructions)
    def printTree(self, indent=0):
        for instruction in self.instructions:
            instruction.printTree(indent)

    @addToClass(AST.Block)
    def printTree(self, indent=0):
        for instruction in self.instructions:
            instruction.printTree(indent)

    @addToClass(AST.Num)
    def printTree(self, indent=0):
        TreePrinter.print_indent_prefix(indent)
        print(self.value)

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        TreePrinter.print_indent_prefix(indent)
        print(self.name)

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        TreePrinter.print_indent_prefix(indent)
        print(self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.UnExpr)
    def printTree(self, indent=0):
        TreePrinter.print_indent_prefix(indent)
        print(self.op)
        self.operand.printTree(indent + 1)

    @addToClass(AST.Assignment)
    def printTree(self, indent=0):
        TreePrinter.print_indent_prefix(indent)
        print(self.op)

        self.ident.printTree(indent)
        self.expression.printTree(indent + 1)

    @addToClass(AST.IdElements)
    def printTree(self, indent=0):
        TreePrinter.print_indent_prefix(indent)
        print("REF")

        TreePrinter.print_indent_prefix(indent + 1)
        print(self.ident)

        for el in self.elements:
            el.printTree(indent + 1)

    @addToClass(AST.Print)
    def printTree(self, indent=0):
        TreePrinter.print_indent_prefix(indent)
        print("PRINT")
        for element in self.to_print:
            element.printTree(indent + 1)

    @addToClass(AST.If)
    def printTree(self, indent=0):
        TreePrinter.print_indent_prefix(indent)
        print("IF")
        self.expression.printTree(indent + 1)
        TreePrinter.print_indent_prefix(indent)
        print("THEN")
        self.instruction1.printTree(indent + 1)
        if self.instruction2 is not None:
            TreePrinter.print_indent_prefix(indent)
            print("ELSE")
            self.instruction2.printTree(indent + 1)

    @addToClass(AST.While)
    def printTree(self, indent=0):
        TreePrinter.print_indent_prefix(indent)
        print("WHILE")
        self.expression.printTree(indent + 1)
        self.instruction.printTree(indent + 1)

    @addToClass(AST.For)
    def printTree(self, indent=0):
        TreePrinter.print_indent_prefix(indent)
        print("FOR")
        self.iterator.printTree(indent + 1)
        TreePrinter.print_indent_prefix(indent + 1)
        print("RANGE")
        self.range_start.printTree(indent + 2)
        self.range_end.printTree(indent + 2)
        self.content.printTree(indent + 1)

    @addToClass(AST.ControlStatement)
    def printTree(self, indent=0):
        TreePrinter.print_indent_prefix(indent)
        print(self.instr)

    @addToClass(AST.Return)
    def printTree(self, indent=0):
        TreePrinter.print_indent_prefix(indent)
        print("RETURN")
        self.expression.printTree()

    @addToClass(AST.String)
    def printTree(self, indent=0):
        TreePrinter.print_indent_prefix(indent)
        print("STRING")
        print(self.content)

    @addToClass(AST.Vector)
    def printTree(self, indent=0):
        TreePrinter.print_indent_prefix(indent)
        print("VECTOR")
        for element in self.elements:
            element.printTree(indent + 1)

    @addToClass(AST.Function)
    def printTree(self, indent=0):
        TreePrinter.print_indent_prefix(indent)
        print(self.func_name)
        self.arguments.printTree(indent + 1)

    @addToClass(AST.ID)
    def printTree(self, indent=0):
        TreePrinter.print_indent_prefix(indent)
        print(self.var_name)
        # if self.row_parameters is not None:
        #     for param in self.row_parameters:
        #         param.printTree(indent + 1)

