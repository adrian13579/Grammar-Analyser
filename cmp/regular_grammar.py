from cmp.automata import *
from cmp.reduce_grammar import epsilon_free
from cmp.pycompiler import *


def new_transitions(trans: {}, G: Grammar, diccionario: {}, end):
    for prod in G.Productions:
        if prod.Right.IsEpsilon:
            continue
        if len(prod.Right) > 2 or (len(prod.Right) == 2 and (prod.Right[0].IsNonTerminal or prod.Right[1].IsTerminal)):
            return None
        if len(prod.Right) == 1 and prod.Right[0].IsNonTerminal:
            return None
        try:
            if len(prod.Right) == 1:
                trans[(diccionario[prod.Left], str(prod.Right[0]))].append(diccionario[end])
            else:
                trans[(diccionario[prod.Left], str(prod.Right[0]))].append(diccionario[prod.Right[1]])

        except:
            if len(prod.Right) == 1:
                trans[(diccionario[prod.Left], str(prod.Right[0]))] = [diccionario[end]]
            else:
                trans[(diccionario[prod.Left], str(prod.Right[0]))] = [diccionario[prod.Right[1]]]
    #trans[(0, 'ε')] = [1]
    for term in G.terminals:
        try:
            a = trans[(1, str(term))]
            trans[(0, term)] = a
        except:
            pass
    return trans


def reg_grammar_to_automaton(G: Grammar):
    G = epsilon_free(G)
    start = G.startSymbol.__str__()
    while True:
        i = 1
        if start + str(i) not in G.symbDict:
            start += str(i)
            break
    end = 'F'
    while True:
        i = 1
        if end + str(i) not in G.symbDict:
            end += str(i)
            break

    diccionario = {}
    diccionario[start] = 0
    for i in range(len(G.nonTerminals)):
        diccionario[G.nonTerminals[i]] = i + 1
    diccionario[end] = len(G.nonTerminals) + 1

    _finals = [diccionario[end]]

    for prod in G.startSymbol.productions:
        if prod.IsEpsilon:
            _finals.append(diccionario[start])

    trans = {}
    trans = new_transitions(trans, G, diccionario, end)
    if trans is None:
        return None
    return NFA(states=len(G.nonTerminals) + 2, finals=_finals, transitions=trans)


def bracket_balanced(_str: str):
    if _str[0] != '(':
        return False

    balance = 0
    for char in _str:
        if char == '(':
            balance += 1
        if char == ')':
            balance -= 1
        if balance == 0 and char != _str[len(_str) - 1]:
            return False
    return True


def take_unnecessary_epsilon(_str: str):
    aux = ''
    for i in range(len(_str)):
        if _str[i] == 'ε':
            if (i == 0 and _str[i + 1] == '|') or (i == len(_str) - 1 and _str[i - 1] == '|'):
                aux += _str[i]

            if i + 1 < len(_str) and i - 1 >= 0:
                if (_str[i - 1] == '|' and _str[i + 1] == '|') or (_str[i - 1] == '|' and _str[i + 1] == ')') or (
                        _str[i - 1] == '(' and _str[i + 1] == '|'):
                    aux += 'ε'
        else:
            aux += _str[i]
    return aux


def transitions_of_rip_state(transitions: {}, i: int):
    come_to_me = set()
    i_go_to = set()
    stay_in_me = None

    for tuple in transitions:
        if transitions[tuple] == [i]:
            if tuple[0] == i:
                stay_in_me = tuple
            else:
                come_to_me.add(tuple)
        elif tuple[0] == i:
            i_go_to.add(tuple)
    return come_to_me, i_go_to, stay_in_me


def DFA_to_GNFA_transitions(transitions: {}, automaton: DFA):
    for dic in automaton.transitions:
        used_destinations = []
        for terminal in automaton.transitions[dic]:
            if automaton.transitions[dic][terminal] in used_destinations:
                continue
            else:
                used_destinations.append(automaton.transitions[dic][terminal])
                dest = automaton.transitions[dic][terminal]
                term = terminal
                for t1 in automaton.transitions[dic]:
                    if t1 == terminal:
                        continue
                    elif automaton.transitions[dic][t1] == dest:
                        term += '|' + t1
                try:
                    transitions[(dic, term)] += dest
                except:
                    transitions[(dic, term)] = dest

    return transitions


def work_with_bridge_transition(transitions: {}, _from, _to, _str):
    aux = None
    for elem in transitions:
        if elem[0] == _from[0] and transitions[elem] == transitions[_to]:
            _str += '|'
            _str += '(' + str(elem[1]) + ')' if str(elem[1]).__len__() > 1 and not bracket_balanced(
                str(elem[1])) else str(elem[1])
            aux = elem
    return aux, _str


def delete_transitions(transitions, come_to_me, i_go_to, stay_in_me):
    for elem in come_to_me:
        del transitions[elem]
    for elem in i_go_to:
        del transitions[elem]
    if stay_in_me is not None:
        del transitions[stay_in_me]
    return transitions


def automaton_to_reg_expression(automaton: DFA):
    transitions = {}
    end = automaton.states

    transitions[(-1, 'ε')] = [0]
    for elem in automaton.finals:
        transitions[(elem, 'ε')] = [end]

    transitions = DFA_to_GNFA_transitions(transitions, automaton)

    for i in range(end):
        come_to_me, i_go_to, stay_in_me = transitions_of_rip_state(transitions, i)
        aux_transitions = {}
        for _from in come_to_me:
            for _to in i_go_to:
                _str = str(_from[1]) if len(_from[1]) <= 1 or bracket_balanced(str(_from[1])) else '(' + str(_from[1]) + ')'
                if _str == 'ε':
                    _str = ''
                if stay_in_me is not None:
                    _str += '(' + str(stay_in_me[1]) + ')*' if not bracket_balanced(str(stay_in_me[1])) and len(
                        stay_in_me[1]) > 1 else str(stay_in_me[1]) + '*'
                if _to[1] == 'ε' and len(_str):
                    do_nothing = 0
                else:
                    _str += str(_to[1]) if len(_to[1]) <= 1 or bracket_balanced(_from[1]) else '(' + str(_to[1]) + ')'
                aux, _str = work_with_bridge_transition(transitions, _from, _to, _str)
                if aux is not None:
                    del transitions[aux]
                aux_transitions[(_from[0], _str)] = transitions[_to]

        transitions = delete_transitions(transitions, come_to_me, i_go_to, stay_in_me)
        transitions.update(aux_transitions)

    _str = ''
    for (origin, text) in transitions:
        _str += text

    return take_unnecessary_epsilon(_str)

# G = Grammar()
# E = G.NonTerminal('E', True)
# T, F, X, Y, Z, W = G.NonTerminals('T F X Y Z W')
# a, b, c = G.Terminals('a b c')

# E %= T + X
# X %= T + X | G.Epsilon | c + T
# T %= F + Y
# F %= a + Y | c + Y | G.Epsilon
# Y %= b + X | a + T
# Z %= b + X | c + Y
# W %= F + b | Z + c

# G = Grammar()
# S = G.NonTerminal('S', True)
# A, B = G.NonTerminals('A B')
# a, b, c = G.Terminals('a b c')
#
# S %= a | a + A | b + B | G.Epsilon
# A %= a + S | a + A
# B %= c + S | G.Epsilon

# # bracket_balanced('(asdfgadjfgasdf()DASdaksdj()')
# dasfhjdasd = reg_grammar_to_automaton(G)
# # print(dasfhjdasd.transitions)
# dasfhjdasd.graph().write_png('auto.png')
#
# dasfhjdasd = nfa_to_dfa(dasfhjdasd)
#
# # dasfhjdasd = DFA(3, [1, 2], {(0, 'a'): 1, (0, 'b'): 2, (1, 'a'): 0, (1, 'b'): 1, (2, 'a'): 1, (2, 'b'): 0})
# dasfhjdasd.graph().write_png('auto1.png')
# # print("DFA")
# #
# print(automaton_to_reg_expression(dasfhjdasd))
# G = Grammar()
# E = G.NonTerminal('E',True)
# T, F = G.NonTerminals('T F')
# plus, star, num, o_par, c_par = G.Terminals('+ * num ( )')
#
# E%= E + plus + T | T
# T%= T + star + F | F
# F%= num | o_par + E + c_par

# dasfhjdasd = reg_grammar_to_automaton(G)
# print(dasfhjdasd.transitions)
# dasfhjdasd.graph().write_png('auto.png')
