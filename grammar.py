from cmp.pycompiler import Grammar, Production, Sentence
from cmp.utils import ContainerSet


def eliminate_left_recursion(G: Grammar):
    recursive_prod = {}
    for production in G.Productions:
        if production.Left == production.Right[0]:
            non_terminal = production.Left
            for prod in non_terminal.productions:
                try:
                    recursive_prod[non_terminal].add(prod)
                except KeyError:
                    recursive_prod[non_terminal] = {prod}

    for non_terminal in recursive_prod.keys():
        new_non_teminal = G.NonTerminals(non_terminal.Name + "'")
        for prod in recursive_prod[non_terminal]:
            new_sentence = Sentence()
            if prod.Right[0] == non_terminal:
                for i in range(1, len(prod.Right)):
                    new_sentence += prod.Right[i]
                new_sentence += new_non_teminal[0]
                new_production = Production(new_non_teminal[0], new_sentence)
                G.Productions.append(new_production)
            else:
                for i in range(len(prod.Right)):
                    new_sentence += prod.Right[i]
                new_sentence += new_non_teminal[0]
                new_production = Production(non_terminal, new_sentence)
                G.Productions.append(new_production)
            G.Productions.remove(prod)
        G.Productions.append(Production(new_non_teminal[0], G.Epsilon))


def remove_useless_non_terminals(G: Grammar):
    usefull_non_terminals = ContainerSet()
    change = True
    while change:
        change = False
        for production in G.Productions:
            for symbol in production.Right:
                if symbol.IsNonTerminal:
                    if symbol not in usefull_non_terminals:
                        break
            else:
                change |= usefull_non_terminals.add(production.Left)
    # TODO se puede mejorar 
    for production in G.Productions:
        if production.Left not in usefull_non_terminals:
            G.Productions.remove(production)
        else:
            for symbol in production.Right:
                if symbol.IsNonTerminal:
                    if symbol not in usefull_non_terminals:
                        G.Productions.remove(production)


def remove_common_prefix(G: Grammar):
    pass


def remove_unreachable_symbols(G: Grammar):
    reachable_symbols = {G.EOF}
    queue = [G.startSymbol]
    while len(queue) != 0:
        current_head = queue[0]
        queue.remove(current_head)

        if current_head not in reachable_symbols:
            reachable_symbols.add(current_head)
            if current_head.IsNonTerminal:
                for production in current_head.productions:
                    for symbol in production.Right:
                        if symbol not in queue:
                            queue.append(symbol)

    unreachable_symbols = []
    for symbol in G.symbDict.values():
        if symbol not in reachable_symbols:
            unreachable_symbols.append(symbol)
            if symbol.IsNonTerminal:
                G.nonTerminals.remove(symbol)
            else:
                G.terminals.remove(symbol)

    for production in G.Productions:
        if production.Left in unreachable_symbols:
            G.Productions.remove(production)
        else:
            for symbol in production.Right:
                if symbol in unreachable_symbols:
                    G.Productions.remove(production)
                    break


def nullable_symbols(G: Grammar) -> ContainerSet:
    _nullable_symbols = ContainerSet()
    change = True
    while change:
        change = False
        for production in G.Productions:
            if production.Right == G.Epsilon or all(symbol in _nullable_symbols for symbol in production.Right):
                change |= _nullable_symbols.add(production.Left)

    return _nullable_symbols


def eliminate_epsilon_productions(G:Grammar):
    
    pass

