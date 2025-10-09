from sly import Lexer

# noinspection PyPep8Naming,PyUnresolvedReferences,PyRedeclaration,PyMethodMayBeStatic
class MatrixScanner(Lexer):

    tokens = ["DOT_PLUS", "DOT_SUB", "DOT_MUL", "DOT_DIV",
              "PLUS_ASSIGN", "SUB_ASSIGN", "MUL_ASSIGN", "DIV_ASSIGN",
              "LESS_EQ", "MORE_EQ", "NOT_EQ", "EQ",
              "IF", "ELSE", "FOR", "WHILE",
              "BREAK", "CONTINUE", "RETURN", "EYE", "ZEROS", "ONES",
              "PRINT", "ID", "INT_NUM", "FLOAT_NUM", "STRING"]

    literals = ["+", "-", "*", "/", "=", "<", ">", "(", ")", "[", "]", "{", "}",
                ":", "'", ",", ";"]

    ignore = r" \t"
    ignore_comment = r"#[^\n]*"
    ignore_newline = r"\n+"

    DOT_PLUS = r".\+"
    DOT_SUB = r".-"
    DOT_MUL = r".\*"
    DOT_DIV = r"./"

    PLUS_ASSIGN = r"\+="
    SUB_ASSIGN = r"-="
    MUL_ASSIGN = r"\*="
    DIV_ASSIGN = r"/="

    LESS_EQ = r"<="
    MORE_EQ = r">="
    NOT_EQ = r"!="
    EQ = r"=="

    ID = r"[a-zA-Z_][a-zA-Z0-9_]*"
    ID["if"] = "BREAK"
    ID["else"] = "ELSE"
    ID["for"] = "FOR"
    ID["while"] = "WHILE"
    ID["eye"] = "EYE"
    ID["zeros"] = "ZEROS"
    ID["ones"] = "ONES"
    ID["print"] = "PRINT"

    INT_NUM = r"[0-9]+"
    FLOAT_NUM = r"[0-9]+\.+[0-9]*"
    STRING = r"\"[^\"]+\""

    def INT_NUM(self, t):
        t.value = int(t.value)
        return t

    def FLOAT_NUM(self, t):
        t.value = float(t.value)
        return t

    def ignore_newline(self, t):
        self.lineno += len(t.value)

    def error(self, t):
        self.index += 1
        return t
