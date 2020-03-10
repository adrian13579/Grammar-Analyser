from cmp.lr1_parser import *
#from cmp.slr1_parser import *
# from cmp.lalr_parser import *
from cmp.ll1_parser import *
from cmp.regular_grammar import *
from cmp.grammar import *

#REVISAR LOS IMPORT ANTES DE EJECUTAR, HAY IMPORT QUE PROVOCAN AMBIGUEDADES SI LOS HACES SIMULTANEOS

##LL1

#Caso1
# G = Grammar()
# E = G.NonTerminal('E', True)
# T, X, F, Y = G.NonTerminals('T X F Y')
# plus, minus, star, div, o_par, c_par, num = G.Terminals('+ - * / ( ) num')
#
# E %= T + X
# X %= plus + T + X | minus + T + X | G.Epsilon
# T %= F + Y
# Y %= star + F + Y | div + F + Y | G.Epsilon
# F %= o_par + E + c_par | num
#
# firsts = compute_firsts(G)
# follows = compute_follows(G, firsts)
# M, _conflict = build_parsing_table(G, firsts, follows)
# #print(conflict_string(G, _conflict[1][0], _conflict[1][1], M, firsts, follows))

#Caso2
# G = Grammar()
# S = G.NonTerminal('S', True)
# A = G.NonTerminal('A')
# a, b, d = G.Terminals('a b d')
#
# S %= a + A
# A %= a + d | d | G.Epsilon
#
# firsts = compute_firsts(G)
# follows = compute_follows(G, firsts)
# M, _conflict = build_parsing_table(G, firsts, follows)
# print(conflict_string(G, _conflict[1][0], _conflict[1][1], M, firsts, follows))

#Caso3
# G = Grammar()
# E = G.NonTerminal('E', True)
# T, X, F, Y = G.NonTerminals('T X F Y')
# plus, minus, star, div, o_par, c_par, num = G.Terminals('plus sub star div o_par c_par num')

# E %= T + X
# X %= plus + T + X | minus + T + X | G.Epsilon
# T %= F + Y
# Y %= star + F + Y | div + F + Y | G.Epsilon
# F %= o_par + E + c_par | num
#
# firsts = compute_firsts(G)
# follows = compute_follows(G, firsts)
# M, _conflict = build_parsing_table(G, firsts, follows)
#print(conflict_string(G, _conflict[1][0], _conflict[1][1], M, firsts, follows))

#Caso4
# G = Grammar()
# E = G.NonTerminal('E', True)
# T, F, X, Y = G.NonTerminals('T F X Y')
# a, b, c = G.Terminals('a b c')
#
# E %= T + X
# X %= T + X | G.Epsilon | c + T
# T %= F + Y
# F %= a + Y | c + Y | G.Epsilon
# Y %= b + X | a + T
# firsts = compute_firsts(G)
# follows = compute_follows(G, firsts)
# M, _conflict = build_parsing_table(G, firsts, follows)
# print(conflict_string(G, _conflict[0][0], _conflict[0][1], M, firsts, follows))

#------------------------------------------------------------

# G = Grammar()
# S = G.NonTerminal('S', True)
# X = G.NonTerminal('X')
# _if, _then, _else, _num = G.Terminals('if then else num')
# S %= _if + X + _then + S
# S %= _if + X + _then + S + _else + S
# S %= _num
# X %= _num
# G=G.AugmentedGrammar()
# #Testing on Shift Reduce Grammars(Para testear tienes q descomentar los respectivos import)
# # adkffadhfksahf = LALR1Parser(G, True)
# # adkffadhfksahf = SLR1Parser(G, True)
# adkffadhfksahf = LR1Parser(G, True)
# terminals = G.terminals
# terminals.append(G.EOF)
# _str = conflict_string_lr1(adkffadhfksahf.action, adkffadhfksahf.goto, terminals)
# print(_str)

# #Testing on LL grammar
# firsts = compute_firsts(G)
# follows = compute_follows(G, firsts)
# M, _conflict = build_parsing_table(G, firsts, follows)
# print(conflict_string(G, _conflict[0][0], _conflict[0][1], M, firsts, follows))

#------------------------------------------------------
#Regular Grammar(esto es para llevar de gramatica reg a exp regular)

# G = Grammar()
# S = G.NonTerminal('S', True)
# A, B = G.NonTerminals('A B')
# a, b, c = G.Terminals('a b c')
#
# S %= a + A | b + B | G.Epsilon
# A %= a + A | c
# B %= b + B | b
#
# dasfhjdasd = reg_grammar_to_automaton(G)
# print(dasfhjdasd.transitions)
# dasfhjdasd.graph().write_png('auto.png')
#
# dasfhjdasd = nfa_to_dfa(dasfhjdasd)
# #
# # #dasfhjdasd = DFA(3, [1, 2], {(0, 'a'): 1, (0, 'b'): 2, (1, 'a'): 0, (1, 'b'): 1, (2, 'a'): 1, (2, 'b'): 0})
# dasfhjdasd.graph().write_png('auto1.png')
# print(automaton_to_reg_expression(dasfhjdasd))

#Entrando directament el automata
#Caso1
# dasfhjdasd = DFA(3, [1, 2], {(0, 'a'): 1, (0, 'b'): 2, (1, 'a'): 0, (1, 'b'): 1, (2, 'a'): 1, (2, 'b'): 0})
# dasfhjdasd.graph().write_png('auto1.png')
# print("DFA")
# print(automaton_to_reg_expression(dasfhjdasd))

#Caso2
# dasfhjdasd = DFA(2, [1], {(0, 'a'): 0, (0, 'b'): 1, (1, 'a'): 1, (1, 'b'): 1})
# dasfhjdasd.graph().write_png('auto1.png')
# print("DFA")
# print(automaton_to_reg_expression(dasfhjdasd))

#Test
G= Grammar()
E = G.NonTerminal('E', True)
num = G.Terminal('num')

E%= num | G.Epsilon

G=G.AugmentedGrammar()
#Testing on Shift Reduce Grammars(Para testear tienes q descomentar los respectivos import)
# adkffadhfksahf = LALR1Parser(G, True)
# adkffadhfksahf = SLR1Parser(G, True)
adkffadhfksahf = LR1Parser(G, True)
terminals = G.terminals
terminals.append(G.EOF)
_str = conflict_string_lr1(adkffadhfksahf.action, adkffadhfksahf.goto, terminals)
print(_str)

