from cmp import first_follow as ff
from cmp.pycompiler import Grammar

G = Grammar()
E = G.NonTerminal('E', True)
T, F, X, Y = G.NonTerminals('T F X Y')
plus, minus, star, div, opar, cpar, num = G.Terminals('+ - * / ( ) num')

E %= T + X
X %= plus + T + X | minus + T + X | G.Epsilon
T %= F + Y
Y %= star + F + Y | div + F + Y | G.Epsilon
F %= num | opar + E + cpar

import cmp.languages

xcool = cmp.languages.BasicXCool(G)

firsts = ff.compute_firsts(G)
assert firsts == xcool.firsts
