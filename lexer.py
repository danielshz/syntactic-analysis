import sys
import re

# REGEX
SPACE = r"\s+"
VARIABLE = r"[a-zA-Z_][a-zA-Z_0-9]*"
EXPRESSION = r"@[^\n]*"
DECIMAL = r"[0-9]+"
OPERADOR = r'%=|//|\*\*|\-=|/=|\*=|\+=|!=|>=|<=|==|<|>|\[|\{|\}|\(|\)|\,|\:|\.|\=|\+|\-|\*|%|/|\]'
COMMENT = r"#[^\n]*"
NEWLINE = r"\n"

regex_list = [
  (COMMENT, 'COMMENT'), 
  (VARIABLE, 'VARIABLE'), 
  (DECIMAL, 'DECIMAL'), 
  (OPERADOR, 'OPERADOR'),
  (EXPRESSION, 'EXPRESSION'),
  (NEWLINE, 'NEWLINE'),
  (SPACE, 'SPACE')
]

def lexical_analysis(code_file, regex_list):
  compile_list = []
  result = []

  for regex, label in regex_list:
    compile_list.append((re.compile(regex), label))
  
  i = 0
  while i < len(code_file):
    has_match = False

    for compile, label in compile_list:
      m = compile.match(code_file, i)

      if not m == None:
        if not label == 'SPACE':
            result.append((label, m.group()))
        i = m.end()
        has_match = True
        break
    
    if not has_match:
      print("ERROR")
      break
  print(result)

try:
  text = open(sys.argv[1], "r")
  code_file = text.read()
  print(code_file)

  lexical_analysis(code_file, regex_list)
except FileNotFoundError as e:
  print(e)
except Exception as e:
  print(e)



