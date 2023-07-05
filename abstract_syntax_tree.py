import math

class EBinary:
    def __init__(self, operand_left, operator, operand_right):
        self.operand_left = operand_left
        self.operator = operator
        self.operand_right = operand_right
        self.type = "Binary"

class ENumber:
    def __init__(self, value):
        self.value = value
        self.type = "Number"

class EUnary:
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand
        self.type = "Unary"

class EVariable:
    def __init__(self, name):
        self.name = name
        self.type = "Variable"

class EParentheses:
    def __init__(self, expression):
        self.expression = expression
        self.type = "Parentheses"

class EFunction:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments
        self.type = "Function"

class EEmpty:
    def __init__(self):
        self.type = "Empty"

class EAssignment:
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression
        self.type = "Assignment"

def evaluate_expression(expression, variables = {}):
    match expression.type:
        case "Binary":
            match expression.operator:
                case "+":
                    return evaluate_expression(expression.operand_left, variables) + evaluate_expression(expression.operand_right, variables)
                case "-":
                    return evaluate_expression(expression.operand_left, variables) - evaluate_expression(expression.operand_right, variables)
                case "*":
                    return evaluate_expression(expression.operand_left, variables) * evaluate_expression(expression.operand_right, variables)
                case "/":
                    return evaluate_expression(expression.operand_left, variables) / evaluate_expression(expression.operand_right, variables)
                case "^":
                    return evaluate_expression(expression.operand_left, variables) ** evaluate_expression(expression.operand_right, variables)
                case _:
                    assert(False)
        case "Number":
            return expression.value
        case "Unary":
            if expression.operator == "+":
                return +evaluate_expression(expression.operand, variables)
            elif expression.operator == "-":
                return -evaluate_expression(expression.operand, variables)
            else:
                assert(False)
        case "Variable":
            assert(expression.name in variables)
            return evaluate_expression(variables[expression.name], variables)
        case "Parentheses":
            return evaluate_expression(expression.expression, variables)
        case "Function":
            match expression.name:                
                case "sin":
                    return math.sin(evaluate_expression(expression.arguments[0], variables))
                case "cos":
                    return math.cos(evaluate_expression(expression.arguments[0], variables))
                case "sqrt":
                    if evaluate_expression(expression.arguments[0], variables) < 0:
                        raise ValueError("Square root of negative number")
                    return math.sqrt(evaluate_expression(expression.arguments[0], variables))
                case _:
                    assert(False)
        case "Empty":
            return 0
        case "Assignment":
            return 0   
        case _:
            assert(False)

def expression_to_string(expression, variables = {}):
    match expression.type:
        case "Binary":
            return "(" + expression_to_string(expression.operand_left, variables) + " " + expression.operator + " " + expression_to_string(expression.operand_right, variables) + ")"
        case "Number":
            return str(expression.value)
        case "Unary":
            return "(" + expression.operator + expression_to_string(expression.operand, variables) + ")"
        case "Variable":
            return expression_to_string(variables[expression.name], variables)
        case "Parentheses":
            return "(" + expression_to_string(expression.expression, variables) + ")"
        case "Function":
            return expression.name + "(" + ", ".join([expression_to_string(argument, variables) for argument in expression.arguments]) + ")"
        case "Empty":
            return ""
        case "Assignment":
            return expression.name + " = " + expression_to_string(expression.expression, variables)
        case _:
            assert(False)

def optimize_expression(expression, variables = {}):
    match expression.type:
        case "Unary":
            if expression.operator == "-":
                if expression.operand.type == "Unary" and expression.operand.operator == "-":
                    return optimize_expression(expression.operand.operand, variables)
            return EUnary(expression.operator, optimize_expression(expression.operand, variables))
        case "Binary":
            if expression.operator == "+":
                if expression.operand_left.type == "Number" and expression.operand_left.value == 0:
                    return optimize_expression(expression.operand_right, variables)
                elif expression.operand_right.type == "Number" and expression.operand_right.value == 0:
                    return optimize_expression(expression.operand_left, variables)
            return EBinary(optimize_expression(expression.operand_left, variables), expression.operator, optimize_expression(expression.operand_right, variables))
        case "Number":
            return expression
        case "Variable":
            return optimize_expression(variables[expression.name], variables)
        case "Parentheses":
            return EParentheses(optimize_expression(expression.expression, variables))
        case "Function":
            return EFunction(expression.name, [optimize_expression(argument, variables) for argument in expression.arguments])
        case "Empty":
            return EEmpty()
        case "Assignment":
            return EAssignment(expression.name, optimize_expression(expression.expression, variables))
        case _:
            assert(False)

# 1 + 2 * 3 = 7
test_expression_1 = EBinary(ENumber(1), "+", EBinary(ENumber(2), "*", ENumber(3))) 

# 1 + 2 * 3 = 9 
test_expression_2 = EBinary(EBinary(ENumber(1), "+", ENumber(2)), "*", ENumber(3))

# (--1) + 0 = 1          
test_expression_3 = EBinary(EUnary("-", EUnary("-", ENumber(1))), "+", ENumber(0))

# A = sin(0)
# A + 5 * 4 = 20
test_expression_4 = EBinary(EVariable("A"), "+", EBinary(ENumber(5), "*", ENumber(4)))
dictionary = {"A": EFunction("sin", [ENumber(0)])}

# a = 10
# b = 20 + 1
# c = 3
# d = sqrt(b+b-4*a*c)
# x1 = (-b + d) / (2*a)
# x2 = (-b - d) / (2*a)
test_expression_5 = EParentheses(EBinary(EBinary(EUnary("-", EVariable("b")), "+", EVariable("d")), "/", EBinary(ENumber(2), "*", EVariable("a"))))
test_expression_6 = EParentheses(EBinary(EBinary(EUnary("-", EVariable("b")), "-", EVariable("d")), "/", EBinary(ENumber(2), "*", EVariable("a"))))
var = {"a": ENumber(10), "b": EBinary(ENumber(20), "+", ENumber(1)), "c": ENumber(3), "d": EFunction("sqrt", [EBinary(EBinary(EVariable("b"), "+", EVariable("b")), "-", EBinary(EBinary(ENumber(4), "*", EVariable("a")), "*", EVariable("c")))])}

# control test

assert(evaluate_expression(test_expression_1) == 7)
assert(evaluate_expression(test_expression_2) == 9)
assert(evaluate_expression(test_expression_3) == 1)
assert(evaluate_expression(test_expression_4, dictionary) == 20)
#sqrt(21-4*10*3) = sqrt(-119) = ValueError
#print(evaluate_expression(test_expression_5, var))
#print(evaluate_expression(test_expression_6, var))

assert(expression_to_string(test_expression_1) == "(1 + (2 * 3))")
assert(expression_to_string(test_expression_2) == "((1 + 2) * 3)")
assert(expression_to_string(test_expression_3) == "((-(-1)) + 0)")
assert(expression_to_string(test_expression_4, dictionary) == "(sin(0) + (5 * 4))")
assert(expression_to_string(test_expression_5, var) == "((((-(20 + 1)) + sqrt((((20 + 1) + (20 + 1)) - ((4 * 10) * 3)))) / (2 * 10)))")
assert(expression_to_string(test_expression_6, var) == "((((-(20 + 1)) - sqrt((((20 + 1) + (20 + 1)) - ((4 * 10) * 3)))) / (2 * 10)))")

assert(expression_to_string(optimize_expression(test_expression_1)) == "(1 + (2 * 3))")
assert(expression_to_string(optimize_expression(test_expression_2)) == "((1 + 2) * 3)")
assert(expression_to_string(optimize_expression(test_expression_3)) == "1")
assert(expression_to_string(optimize_expression(test_expression_4, dictionary)) == "(sin(0) + (5 * 4))")
assert(expression_to_string(optimize_expression(test_expression_5, var)) == "((((-(20 + 1)) + sqrt((((20 + 1) + (20 + 1)) - ((4 * 10) * 3)))) / (2 * 10)))")
assert(expression_to_string(optimize_expression(test_expression_6, var)) == "((((-(20 + 1)) - sqrt((((20 + 1) + (20 + 1)) - ((4 * 10) * 3)))) / (2 * 10)))")