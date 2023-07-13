import math
variable = {}

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
        variable[name] = expression

class Token:
    def __init__(self, value, type, line, column):
        self.value = value
        self.type = type
        self.line = line
        self.column = column

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
        self.next_token = tokens[self.index]
        
    def peek(self, type):
        return self.next_token.type == type
    
    def consume(self, type):
        if self.peek(type):
            self.index += 1
            self.next_token = self.tokens[self.index]
            return self.tokens[self.index - 1]
        else:
            raise SyntaxError("Expected token of type " + type + " at line " + str(self.next_token.line) + " column " + str(self.next_token.column))
    
    def parseVS(self):
        while self.peek("VARIABLE"):
            v = self.consume("VARIABLE")
            self.consume("EQUAL")
            e = self.parseE()
            return EAssignment(v.value, e)
        else:
            return EEmpty()
        
    def parsePS(self):
        while self.peek("PRINT"):
            self.consume("PRINT")
            e = self.parseE()
            return e
        else:
            return EEmpty()

    def parseS(self):
        if self.peek("VARIABLE"):
            return self.parseVS()
        if self.peek("PRINT"):
            return self.parsePS()
        else:
            raise SyntaxError("Expected token of type VARIABLE or PRINT at line " + str(self.next_token.line) + " column " + str(self.next_token.column))

    def parseE(self):
        e = self.parseT()
        while True:
            if self.peek("EOF"):
                return e
            elif self.peek("SUM"):
                self.consume("SUM")
                e = EBinary(e, "+", self.parseT())
            elif self.peek("SUB"):
                self.consume("SUB")
                e = EBinary(e, "-", self.parseT())
            else:
                break
        return e
    
    def parseT(self):
        e = self.parseF()
        while True:
            if self.peek("EOF"):
                return e
            elif self.peek("MULT"):
                self.consume("MULT")
                e = EBinary(e, "*", self.parseF())
            elif self.peek("DIV"):
                self.consume("DIV")
                e = EBinary(e, "/", self.parseF())
            else:
                break
        return e
    
    def parseF(self):
        if self.peek("NUM"):
            n = self.consume("NUM")
            return ENumber(int(n.value))
        
        elif self.peek("VARIABLE"):
            v = self.consume("VARIABLE")
            return EVariable(v.value)
                        
        elif self.peek("PARENTESES_L"):
            self.consume("PARENTESES_L")
            e = self.parseE()
            self.consume("PARENTESES_R")
            return EParentheses(e)
            
        elif self.peek("SUB"):
            self.consume("SUB")
            e = self.parseF()
            return EUnary("-", e)
        
        elif self.peek("FUNCTION"):
            function = self.consume("FUNCTION").value
            if self.peek("PARENTESES_L"):
                self.consume("PARENTESES_L")
                e = self.parseE()
                self.consume("PARENTESES_R")
                return EFunction(function, [e])

def evaluate_expression(expression, variables = variable):
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
                
                case "tan":
                    return math.tan(evaluate_expression(expression.arguments[0], variables))
                
                case "sqrt":
                    if evaluate_expression(expression.arguments[0], variables) < 0:
                        raise ValueError("Square root of negative number")
                    return math.sqrt(evaluate_expression(expression.arguments[0], variables))
                
                case _:
                    assert(False)

        case "Empty":
            return 0
        
        case "Assignment":
            return evaluate_expression(expression.expression, variables) 
        
        case _:
            assert(False)

def expression_to_string(expression, variables = variable):
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

def optimize_expression(expression, variables = variable):
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


