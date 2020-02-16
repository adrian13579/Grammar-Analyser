from lexer import Lexer

lexer = Lexer([('A', 'a|b|c|d')], 'eof')

tokens = lexer('abc')

print(tokens)
