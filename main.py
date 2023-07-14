import lexer
import sys 
import fileinput
from abstract_syntax_tree import *
from test import *

def lexer_token(code_file):
    lista = lexer.lexical_analysis(code_file)
    
    #Filtrar lista
    tokens = []
    result = []
    i = 0
    j = 0
    for l in lista:
        token = Token(l[1], l[0], i, j)
        #print("coloquei o token: ", token.type, token.value, token.line, token.column)
        tokens.append(token)
        j += 1
        if token.type == "NEWLINE":
            result.append(tokens)
            tokens = []
            i += 1
            j = 0
    result.append(tokens)
    return result

if __name__ == "__main__":
    #Entrada pelo input padrão
    if len(sys.argv) < 2:
        result = []
        for line in fileinput.input():
            result.append(line)
        result = lexer_token("".join(result))

    #Rotina de teste
    elif sys.argv[1] ==  "-test":
        print("Iniciando rotina de teste...\n")
        test = Test()
        test.control_test()
        test.lexer_test()
        test.evaluation_test()
        print("Testes concluídos com sucesso!")
        exit()

    #Entrada por argumento
    else:
        try:
            text = open(sys.argv[1], "r")
            code_file = text.read()
            result = lexer_token(code_file)
        except Exception as e:
            print(e)
   
    for tokens in result:  # type: ignore
            parser = Parser(tokens).parseS()
            if tokens[0].type == "PRINT":
                print(f'''\n{expression_to_string(parser)}\n=> {evaluate_expression(parser)}\n====================''')