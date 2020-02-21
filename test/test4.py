from lexer import Lexer

lexer = Lexer([('A', '(a|b)')], 'eof')

tokens = lexer('ab')
lexer.automaton.graph().write_png('a.png')
print(tokens)
