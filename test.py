import lexer
from abstract_syntax_tree import *
import main
import os

class Test:
    def control_test(self):
        # 1 + 2 * 3 = 7
        test_expression_1 = EBinary(ENumber(1), "+", EBinary(ENumber(2), "*", ENumber(3))) 

        # 1 + 2 * 3 = 9 
        test_expression_2 = EBinary(EBinary(ENumber(1), "+", ENumber(2)), "*", ENumber(3))

        # (--1) + 0 = 1          
        test_expression_3 = EBinary(EUnary("-", EUnary("-", ENumber(1))), "+", ENumber(0))

        # A = sin(0)
        # A + 5 * 4 = 20
        test_expression_4 = EBinary(EVariable("A"), "+", EBinary(ENumber(5), "*", ENumber(4)))
        variables_exp_4 = {"A": EFunction("sin", [ENumber(0)])}

        # a = 10
        # b = 20 + 1
        # c = 3
        # d = sqrt(b*b-4*a*c)
        # x1 = (-b + d) / (2*a)
        # x2 = (-b - d) / (2*a)
        test_expression_5 = EParentheses(EBinary(EBinary(EUnary("-", EVariable("b")), "+", EVariable("d")), "/", EBinary(ENumber(2), "*", EVariable("a"))))
        test_expression_6 = EParentheses(EBinary(EBinary(EUnary("-", EVariable("b")), "-", EVariable("d")), "/", EBinary(ENumber(2), "*", EVariable("a"))))
        variables_exp_5 = {"a": ENumber(10), "b": EBinary(ENumber(20), "+", ENumber(1)), "c": ENumber(3), "d": EFunction("sqrt", [EBinary(EBinary(EVariable("b"), "*", EVariable("b")), "-", EBinary(EBinary(ENumber(4), "*", EVariable("a")), "*", EVariable("c")))])}

        assert(evaluate_expression(test_expression_1) == 7)
        assert(evaluate_expression(test_expression_2) == 9)
        assert(evaluate_expression(test_expression_3) == 1)
        assert(evaluate_expression(test_expression_4, variables_exp_4) == 20)
        assert(evaluate_expression(test_expression_5, variables_exp_5) == -0.15417635664155416)
        assert(evaluate_expression(test_expression_6, variables_exp_5) == -1.945823643358446)

        assert(expression_to_string(test_expression_1) == "(1 + (2 * 3))")
        assert(expression_to_string(test_expression_2) == "((1 + 2) * 3)")
        assert(expression_to_string(test_expression_3) == "((-(-1)) + 0)")
        assert(expression_to_string(test_expression_4, variables_exp_4) == "(sin(0) + (5 * 4))")
        assert(expression_to_string(test_expression_5, variables_exp_5) == "((((-(20 + 1)) + sqrt((((20 + 1) * (20 + 1)) - ((4 * 10) * 3)))) / (2 * 10)))")
        assert(expression_to_string(test_expression_6, variables_exp_5) == "((((-(20 + 1)) - sqrt((((20 + 1) * (20 + 1)) - ((4 * 10) * 3)))) / (2 * 10)))")

        assert(expression_to_string(optimize_expression(test_expression_1)) == "(1 + (2 * 3))")
        assert(expression_to_string(optimize_expression(test_expression_2)) == "((1 + 2) * 3)")
        assert(expression_to_string(optimize_expression(test_expression_3)) == "1")
        assert(expression_to_string(optimize_expression(test_expression_4, variables_exp_4)) == "(sin(0) + (5 * 4))")
        assert(expression_to_string(optimize_expression(test_expression_5, variables_exp_5)) == "((((-(20 + 1)) + sqrt((((20 + 1) * (20 + 1)) - ((4 * 10) * 3)))) / (2 * 10)))")
        assert(expression_to_string(optimize_expression(test_expression_6, variables_exp_5)) == "((((-(20 + 1)) - sqrt((((20 + 1) * (20 + 1)) - ((4 * 10) * 3)))) / (2 * 10)))")

        print("Testes de controle concluídos com sucesso!")

    def lexer_test(self):
        assert(lexer.lexical_analysis("1 + 2 * 3") == [('NUM', '1'), ('SUM', '+'), ('NUM', '2'), ('MULT', '*'), ('NUM', '3'), ('EOF', 'EOF')])
        print("Lexer testado com sucesso!\n")
    
    def parser_test(self):
        try:
            error_test_1 = main.read_file_tokens("@1 +* 2")
            main.Parser(error_test_1[0]).parseS()
        except Exception as e:
            print(e)

        try:
            error_test_2 = main.read_file_tokens("@1 + 2 *")
            main.Parser(error_test_2[0]).parseS()
        except Exception as e:
            print(e)
        
        try:
            error_test_3 = main.read_file_tokens("@1 2 * 3")
            main.Parser(error_test_3[0]).parseS()
        except Exception as e:
            print(e)

        print("Parser testado com sucesso!\n")
        return

    def evaluation_test(self):
        # Carrega os arquivos de teste na pasta tests
        for file in os.listdir(os.path.dirname(__file__) + "/tests"):
            if file.endswith(".txt"):
                print(f"  Testando arquivo {file}...")
                text = open(os.path.dirname(__file__) + "/tests/" + file, "r")
                code_file = text.read()
                result = main.read_file_tokens(code_file)
                
                for tokens in result:
                    parser = main.Parser(tokens).parseS()

                    # Não testar linhas vazias
                    if parser == None or parser.type == "Empty":
                        continue
                    print(f'''{expression_to_string(parser)}\n=> {evaluate_expression(parser)}\n====================''')
        
        print("Testes de leitura e avaliação concluídos com sucesso!\n")