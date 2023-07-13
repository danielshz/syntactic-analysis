import test, lexer
import sys 
from abstract_syntax_tree import *

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
    result.append(tokens)
    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Argumentos inválidos")
         
    elif sys.argv[1] ==  "-test":
        test.Test()
    else:
        try:
            text = open(sys.argv[1], "r")
            code_file = text.read()
            #print(code_file)
            result = lexer_token(code_file)

            for tokens in result:
                parser = Parser(tokens).parseS()
                #print(parser)
                print(f'''{expression_to_string(parser)}
=> {evaluate_expression(parser)}
==================== ''')
            
        except Exception as e:
            print(e)