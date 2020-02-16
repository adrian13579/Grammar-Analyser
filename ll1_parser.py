from first_follow import compute_firsts, compute_follows


def metodo_predictivo_no_recursivo(G, M):
    parser = deprecated_metodo_predictivo_no_recursivo(G, M)

    def updated(tokens):
        return parser([t.token_type for t in tokens])

    return updated


def deprecated_metodo_predictivo_no_recursivo(G, M=None, firsts=None, follows=None):
    if M is None:
        if firsts is None:
            firsts = compute_firsts(G)
        if follows is None:
            follows = compute_follows(G, firsts)
        M = build_parsing_table(G, firsts, follows)

    def parser(w):
        stack = [G.startSymbol]
        cursor = 0
        output = []
        while len(stack) != 0:
            top = stack.pop()
            a = w[cursor]
            if top.IsTerminal:
                if a == top:
                    cursor += 1
                else:
                    raise Exception("Parsing error")
            elif top.IsNonTerminal:
                production = M[top, a]
                for i in reversed(production[0].Right):
                    stack.append(i)
                output.append(production[0])
        return output

    return parser


def build_parsing_table(G, firsts, follows):
    M = {}

    for production in G.Productions:
        X = production.Left
        alpha = production.Right

        for terminal in G.terminals:
            if terminal in firsts[alpha].set:
                M[X, terminal] = [production]
            if firsts[alpha].contains_epsilon and terminal in follows[X]:
                M[X, terminal] = [production]

        if firsts[alpha].contains_epsilon and G.EOF in follows[X]:
            M[X, G.EOF] = [production]

    return M
