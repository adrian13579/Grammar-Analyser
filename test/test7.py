from cmp.first_follow import compute_firsts, compute_follows
from cmp.grammar import remove_useless_non_terminals, eliminate_left_recursion, remove_common_prefix
from cmp.pycompiler import Grammar
from cmp.regular_grammar import reg_grammar_to_automaton, State

G = Grammar()
S = G.NonTerminal('S', True)
A, B = G.NonTerminals('A B')
a, b, c = G.Terminals('a b c')

# S %= a | a + A | b + B | G.Epsilon
# A %= a + S | a + A
# B %= c + S | G.Epsilon
# S %= A
S %= a + S
S %= G.Epsilon
print(G)

# a = compute_firsts(G)
# b = compute_follows(G, a)
#
# automaton = reg_grammar_to_automaton(G)
# automaton = State.from_nfa(automaton)
# automaton.write_to('a.svg')
# eliminate_left_recursion(G)
remove_common_prefix(G)
print(G)

print(12)