import lexer
import sys 
import fileinput
from abstract_syntax_tree import *
from test import *

def read_file_tokens(code_file):
    lexer_tokens = lexer.lexical_analysis(code_file)
    
    line_tokens = []
    file_tokens = []

    i, j = 0, 0

    for label, value  in lexer_tokens:
        token = Token(value, label, i, j)
        line_tokens.append(token)
        j += 1

        if token.type == "NEWLINE":
            file_tokens.append(line_tokens)
            line_tokens = []
            i += 1
            j = 0

    file_tokens.append(line_tokens)

    return file_tokens

if __name__ == "__main__":
    tokens = []

    # Entrada pelo input padrão
    if len(sys.argv) < 2:
        for line in fileinput.input():
            tokens.append(line)
        tokens = read_file_tokens("".join(tokens))

    # Rotina de teste
    elif sys.argv[1] ==  "-test":
        print("Iniciando rotina de teste...\n")
        test = Test()
        
        test.control_test()
        test.lexer_test()
        test.evaluation_test()

        print("Testes concluídos com sucesso!")
        exit()

    # Entrada por argumento
    else:
        try:
            text = open(sys.argv[1], "r")
            code_file = text.read()
            tokens = read_file_tokens(code_file)
        except Exception as e:
            print(e)

   # type: ignore
    for tokens in tokens:  
            parser = Parser(tokens).parseS()
            if tokens[0].type == "PRINT":
                print(f'''\n{expression_to_string(parser)}\n=> {evaluate_expression(parser)}\n====================''')