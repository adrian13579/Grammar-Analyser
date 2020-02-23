from lexer import Lexer

lexer = Lexer([('A', '(a|b|c)*'),('space','drian')], 'eof')

tokens = lexer('abcdrian')
lexer.automaton.graph().write_png('a.png')
print(tokens)
