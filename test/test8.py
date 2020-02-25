from cmp.grammar import remove_common_prefix
from cmp.pycompiler import Grammar
from cmp.regular_grammar import reg_grammar_to_automaton, State

G = Grammar()
S = G.NonTerminal('S', True)
A, B = G.NonTerminals('A B')
a, b, c = G.Terminals('a b c')

S %= A + B
A %= a + b + A
A %= a + b + B
B %= G.Epsilon
B %= b
# S %= a | a + A | b + B | G.Epsilon
# A %= a + S | a + A
# B %= c + S | G.Epsilon
# S %= A

remove_common_prefix(G)


print(12)