#!/usr/bin/python

class Symbol:
    def __init__(self, name, element_type):
        self.name = name
        self.element_type = element_type


class VariableSymbol(Symbol):

    def __init__(self, name, element_type, size=None):
        super().__init__(name, element_type)
        self.size = size


class SymbolTable(object):
    def __init__(self, parent, name): # parent scope and symbol table name
        self.parent = parent
        self.name = name
        self.symbols = {}

    def put(self, name, symbol): # put variable symbol or fundef under <name> entry
        self.symbols[name] = symbol

    def get(self, name): # get variable symbol or fundef from <name> entry
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.get(name)
        return None

    def getParentScope(self):
        return self.parent

    def pushScope(self, name):
        child = SymbolTable(self, name)
        return child

    def popScope(self):
        return self.parent


