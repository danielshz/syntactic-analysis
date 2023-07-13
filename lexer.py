import re

# REGEX
SPACE = r"\s+"
VARIABLE = r"[a-zA-Z_][a-zA-Z_0-9]*"
PRINT = r"@"
NUM = r"[0-9]+"
PARENTESES_L = r'\('
PARENTESES_R = r'\)'
EQUAL = r'\='
SUM = r'\+'
SUB = r'\-'
MULT = r'\*'
DIV = r'\/'
COMMENT = r"#[^\n]*"
NEWLINE = r"\n"
#EOF = r"$"

regex_list = [
  (COMMENT, 'COMMENT'), 
  (VARIABLE, 'VARIABLE'),
  (NUM, 'NUM'), 
  (PARENTESES_L, 'PARENTESES_L'),
  (PARENTESES_R, 'PARENTESES_R'),
  (EQUAL, 'EQUAL'),
  (SUM, 'SUM'),
  (SUB, 'SUB'),
  (MULT, 'MULT'),
  (DIV, 'DIV'),
  (PRINT, 'PRINT'),
  (NEWLINE, 'NEWLINE'),
  (SPACE, 'SPACE')
]

keywords = {"sqrt", "sin", "cos", "tan"}

def lexical_analysis(code_file, regex_list = regex_list, keywords = keywords):
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
          if label == 'VARIABLE' and m.group() in keywords:
            label = 'FUNCTION'
          result.append((label, m.group()))
        i = m.end()
        has_match = True
        break
    
    if not has_match:
      print("ERROR: Unexpected character in input: %r" % code_file[i])
      break
  result.append(('EOF', 'EOF'))
  return result





