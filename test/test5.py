import first_follow as ff
from cmp.pycompiler import Grammar
from grammar import eliminate_left_recursion, remove_useless_non_terminals, remove_unreachable_symbols, nullable_symbols

G = Grammar()
E = G.NonTerminal('E', True)
T, F, X, Y = G.NonTerminals('T F X Y')
plus, minus, star, div, opar, cpar, num = G.Terminals('+ - * / ( ) num')

E %= T + X | Y
T %= plus + T | plus
X %= minus + X
Y %= star
T %= T + plus | G.Epsilon
# X %= plus + T + X | minus + T + X
# T %= F + Y
# Y %= star + F + Y | div + F + Y
# F %= num | opar + E + cpar
#eliminate_left_recursion(G)
#remove_useless_non_terminals(G)
#remove_unreachable_symbols(G)
a = nullable_symbols(G)
print(a)