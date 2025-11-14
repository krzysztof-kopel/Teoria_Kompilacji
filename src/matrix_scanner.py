from sly import Lexer

# noinspection PyPep8Naming,PyUnresolvedReferences,PyRedeclaration,PyMethodMayBeStatic
class MatrixScanner(Lexer):

    tokens = ["DOT_PLUS", "DOT_SUB", "DOT_MUL", "DOT_DIV",
              "PLUS_ASSIGN", "SUB_ASSIGN", "MUL_ASSIGN", "DIV_ASSIGN",
              "LESS_EQ", "MORE_EQ", "NOT_EQ", "EQ",
              "IF", "ELSE",  "FOR", "WHILE",
              "BREAK", "CONTINUE", "RETURN", "EYE", "ZEROS", "ONES",
              "PRINT", "ID", "INT_NUM", "FLOAT_NUM", "STRING"]

    literals = ["+", "-", "*", "/", "=", "<", ">", "(", ")", "[", "]", "{", "}",
                ":", "'", ",", ";"]

    ignore = r" \t"
    ignore_comment = r"#.*"
    @_("\n+")
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    DOT_PLUS = r"\.\+"
    DOT_SUB = r"\.-"
    DOT_MUL = r"\.\*"
    DOT_DIV = r"\./"

    PLUS_ASSIGN = r"\+="
    SUB_ASSIGN = r"-="
    MUL_ASSIGN = r"\*="
    DIV_ASSIGN = r"/="

    LESS_EQ = r"<="
    MORE_EQ = r">="
    NOT_EQ = r"!="
    EQ = r"=="

    ID = r"[a-zA-Z_][a-zA-Z0-9_]*"
    ID["if"] = "IF"
    ID["break"] = "BREAK"
    ID["else"] = "ELSE"
    ID["for"] = "FOR"
    ID["while"] = "WHILE"
    ID["return"] = "RETURN"
    ID["continue"] = "CONTINUE"
    ID["eye"] = "EYE"
    ID["zeros"] = "ZEROS"
    ID["ones"] = "ONES"
    ID["print"] = "PRINT"

    @_(r"([0-9]+\.([0-9]*([eE][+-]?[0-9]+)?))|([0-9]*\.[0-9]+([eE][+-]?[0-9]+)?)")
    def FLOAT_NUM(self, t):
        t.value = float(t.value)
        return t

    @_(r"[0-9]+")
    def INT_NUM(self, t):
        t.value = int(t.value)
        return t

    STRING = r"\"[^\"\n]+\""

    def error(self, t):
        self.index += 1
        return t
