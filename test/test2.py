from cmp.derivation_tree import derivation_tree_ll
from cmp.pycompiler import Production, Sentence, Grammar
from cmp.first_follow import compute_firsts, compute_follows
from cmp.ll1_parser import build_parsing_table, deprecated_metodo_predictivo_no_recursivo

G = Grammar()
E = G.NonTerminal('E', True)
T, F, X, Y = G.NonTerminals('T F X Y')
plus, minus, star, div, opar, cpar, num = G.Terminals('+ - * / ( ) num')

E %= T + X
X %= plus + T + X | minus + T + X | G.Epsilon
T %= F + Y
Y %= star + F + Y | div + F + Y | G.Epsilon
F %= num | opar + E + cpar
print(G)

firsts = compute_firsts(G)
follows = compute_follows(G, firsts)
M = build_parsing_table(G, firsts, follows)
parser = deprecated_metodo_predictivo_no_recursivo(G, M)
left_parse = parser([num, star, num, star, num, plus, num, star, num, plus, num, plus, num, G.EOF])

tree,_ = derivation_tree_ll(left_parse, -1)

tree.write_to('a.svg')
# assert left_parse == [
#     Production(E, Sentence(T, X)),
#     Production(T, Sentence(F, Y)),
#     Production(F, Sentence(num)),
#     Production(Y, Sentence(star, F, Y)),
#     Production(F, Sentence(num)),
#     Production(Y, Sentence(star, F, Y)),
#     Production(F, Sentence(num)),
#     Production(Y, G.Epsilon),
#     Production(X, Sentence(plus, T, X)),
#     Production(T, Sentence(F, Y)),
#     Production(F, Sentence(num)),
#     Production(Y, Sentence(star, F, Y)),
#     Production(F, Sentence(num)),
#     Production(Y, G.Epsilon),
#     Production(X, Sentence(plus, T, X)),
#     Production(T, Sentence(F, Y)),
#     Production(F, Sentence(num)),
#     Production(Y, G.Epsilon),
#     Production(X, Sentence(plus, T, X)),
#     Production(T, Sentence(F, Y)),
#     Production(F, Sentence(num)),
#     Production(Y, G.Epsilon),
#     Production(X, G.Epsilon),
# ]
# for derivation in left_parse:
#     print(derivation)
# for key_value in M:
#     print(key_value, M[key_value])
