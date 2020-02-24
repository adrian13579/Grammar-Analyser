from cmp.derivation_tree import derivation_tree_lr
from cmp.pycompiler import Grammar
from cmp.slr1_parser import build_LR0_automaton, SLR1Parser

G = Grammar()
E = G.NonTerminal('E', True)
T, F = G.NonTerminals('T F')
plus, minus, star, div, opar, cpar, num = G.Terminals('+ - * / ( ) int')

E %= E + plus + T | T  # | E + minus + T
T %= T + star + F | F  # | T + div + F
F %= num | opar + E + cpar

GG = G.AugmentedGrammar()

assert len(GG.startSymbol.productions) == 1
start_production = GG.startSymbol.productions[0]
automaton = build_LR0_automaton(GG)

parser = SLR1Parser(G, verbose=True)

derivation = parser([num, plus, num, star, num, G.EOF])

assert str(derivation) == '[F -> int, T -> F, E -> T, F -> int, T -> F, F -> int, T -> T * F, E -> E + T]'

tree,_ = derivation_tree_lr(derivation, len(derivation))
tree.write_to('b.svg')
