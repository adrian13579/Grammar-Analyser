from cmp.pycompiler import Grammar
from cmp.grammar import eliminate_left_recursion

G = Grammar()
E = G.NonTerminal('E', True)
r = G.NonTerminals('wrwfw')
T, F, X, Y = G.NonTerminals('T F X Y')
plus, minus, star, div, opar, cpar, num = G.Terminals('+ - * / ( ) num')

E %= T + X
T %= T + X
T %= T + plus
# X %= plus + T + X | minus + T + X
T %= F + Y
# Y %= star + F + Y | div + F + Y
# F %= num | opar + E + cpar

eliminate_left_recursion(G)
print(G)