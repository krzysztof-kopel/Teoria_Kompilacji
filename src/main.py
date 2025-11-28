from src.matrix_scanner import MatrixScanner
from src.matrix_parser import MatrixParser

file_name = input("File with code: ").strip()

with open(f"..\\tests\\{file_name}") as file:
    program_text = file.read()

lexer = MatrixScanner()
for token in lexer.tokenize(program_text):
    if str(token.type) != "ERROR":
        print(f"({token.lineno}): {token.type}({token.value})")
    else:
        print(f"Error: unknown token starting at {token.value[0:min(5, len(token.value), token.value.find("\n"))]}")

parser = MatrixParser()
tokens = parser.parse(lexer.tokenize(program_text))

if not parser.error_occurred and tokens is not None:
    print("Abstract syntax tree:")
    tokens.printTree()
