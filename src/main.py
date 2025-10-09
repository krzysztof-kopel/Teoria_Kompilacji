from src.matrix_scanner import MatrixScanner

file_name = input("File with code: ").strip()

with open(f"..\\tests\\{file_name}.m") as file:
    program_text = file.read()

lexer = MatrixScanner()
for token in lexer.tokenize(program_text):
    if str(token.type) != "ERROR":
        print(f"({token.lineno}): {token.type}({token.value})")
    else:
        print(f"Error: unknown character value {token.value[0]}")
