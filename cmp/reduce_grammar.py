from cmp.pycompiler import *


def derivate_directly_epsilon(G: Grammar):
    _ret = set()
    for prod in G.Productions:
        if prod.IsEpsilon:
            _ret.add(prod.Left)
    return _ret


def derivate_indirectly_epsilon(G: Grammar, der_eps: set):
    change = True
    while change:
        change = False
        for prod in G.Productions:
            for elem in prod.Right:
                if elem not in der_eps:
                    break
            else:
                if prod.Left not in der_eps:
                    der_eps.add(prod.Left)
                    change = True

    return der_eps


def create_new_production(elem: NonTerminal, prod: Production):
    sentence = None
    for symbol in prod.Right:
        if symbol == elem:
            continue
        else:
            if sentence is None:
                sentence = symbol
            else:
                sentence += symbol
    if sentence is not None:
        prod.Left %= sentence


def remove_epsilon_productions(G):
    remove = []
    for prod in G.Productions:
        if prod.IsEpsilon:
            remove.append(prod)
    for prod in remove:
        prod.Left.productions.remove(prod)
        G.Productions.remove(prod)


def swap_production(prod, sentence, G):
    if sentence is not None:
        for aux_prod in prod.Left.productions:
            if len(sentence) == 1:
                if len(aux_prod.Right) == 1 and sentence == aux_prod.Right[0]:
                    break
            elif aux_prod.Right == sentence:
                break
        else:
            prod.Left %= sentence
    prod.Left.productions.remove(prod)
    G.Productions.remove(prod)


def eliminate_unnecessary_nonTerminals_epsilon_free(G: Grammar):
    change = True
    while change:
        change = False
        for prod in G.Productions:
            sentence = None
            change_production = False
            for elem in prod.Right:
                if elem.IsTerminal or len(elem.productions):
                    if sentence is None:
                        sentence = elem
                    else:
                        sentence += elem
                else:
                    change = True
                    change_production = True
            if change_production:
                swap_production(prod, sentence, G)
                change_production = False
    return G


def epsilon_free(G: Grammar):
    set = derivate_directly_epsilon(G)
    set = derivate_indirectly_epsilon(G, set)
    remove_epsilon_productions(G)
    for elem in set:
        for prod in G.Productions:
            if elem in prod.Right:
                create_new_production(elem, prod)
    eliminate_unnecessary_nonTerminals_epsilon_free(G)
    if G.startSymbol in set:
        G.startSymbol %= G.Epsilon
    return G


def eliminate_unnecessary_productions(G: Grammar):
    _used = reachable_from_startSymbol(G)
    remove_nonTerminal = []
    for nonTerminal in G.nonTerminals:
        if nonTerminal not in _used:
            for prod in nonTerminal.productions:
                G.Productions.remove(prod)
            remove_nonTerminal.append(nonTerminal)
    for nonTerminal in remove_nonTerminal:
        G.nonTerminals.remove(nonTerminal)
    return G


def reachable_from_startSymbol(G):
    _used = set()
    _used.add(G.startSymbol)
    next_level = [G.startSymbol]
    change = True
    while change:
        change = False
        aux = []
        for symbol in next_level:
            if symbol.IsNonTerminal:
                for production in symbol.productions:
                    for elem in production.Right:
                        if elem not in _used:
                            aux.append(elem)
                            _used.add(elem)
                            change = True
        next_level = aux
    return _used


G = Grammar()
E = G.NonTerminal('E', True)
T, F, X, Y, Z, W = G.NonTerminals('T F X Y Z W')
a, b, c = G.Terminals('a b c')

E %= T + X
X %= T + X | G.Epsilon | c + T
T %= F + Y
F %= a + Y | c + Y | G.Epsilon
Y %= b + X | a + T | G.Epsilon
Z %= b + X | c + Y
W %= F + b | Z + c
print(G)
print(epsilon_free(G))
# print(eliminate_unnecessary_productions(G))
print('a')
