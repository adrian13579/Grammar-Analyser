from cmp.pycompiler import Grammar, Production


def eliminate_left_recursion(G: Grammar):  # -> Grammar:
    recursive_prod = {}
    for production in G.Productions:
        if production.Left == production.Right[0]:
            try:
                recursive_prod[production.Left].append(production)
            except KeyError:
                recursive_prod[production.Left] = [production]


