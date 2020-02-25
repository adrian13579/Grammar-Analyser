from cmp.first_follow import compute_firsts, compute_follows
from cmp.pycompiler import Grammar, Symbol, NonTerminal, Terminal


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
        M, _ = build_parsing_table(G, firsts, follows)

    # def parser(w):
    #     stack = [G.startSymbol]
    #     cursor = 0
    #     output = []
    #     while len(stack) != 0:
    #         top = stack.pop()
    #         a = w[cursor]
    #         if top.IsTerminal:
    #             if a == top:
    #                 cursor += 1
    #             else:
    #                 raise Exception("Parsing error")
    #         elif top.IsNonTerminal:
    #             production = M[top, a]
    #             for i in reversed(production[0].Right):
    #                 stack.append(i)
    #             output.append(production[0])
    #     return output
    def parser(w):
        stack = [G.EOF, G.startSymbol]
        cursor = 0
        output = []

        while True:
            # print(stack, cursor)
            top = stack.pop()
            a = w[cursor]

            if top.IsEpsilon:
                pass
            elif top.IsTerminal:
                assert top == a
                if top == G.EOF:
                    break
                cursor += 1
            else:
                try:
                    production = M[top, a][0]
                    output.append(production)
                    production = list(production.Right)
                    stack.extend(production[::-1])
                except:
                    return

        return output

    return parser

#
# def build_parsing_table(G, firsts, follows):
#     # init parsing table
#     M = {}
#
#     # P: X -> alpha
#     for production in G.Productions:
#         X = production.Left
#         alpha = production.Right
#
#         for terminal in G.terminals:
#             if terminal in firsts[alpha].set:
#                 M[X, terminal] = [production]
#             if firsts[alpha].contains_epsilon and terminal in follows[X]:
#                 M[X, terminal] = [production]
#
#         if firsts[alpha].contains_epsilon and G.EOF in follows[X]:
#             M[X, G.EOF] = [production]
#
#     # parsing table is ready!!!
#     return M,[]

def build_parsing_table(G, firsts, follows):
    M = {}
    _conflict = []
    for production in G.Productions:
        X = production.Left
        alpha = production.Right

        for terminal in G.terminals:

            try:
                _try = M[X, terminal]
            except KeyError:
                M[X, terminal] = []

            if terminal in firsts[alpha].set:
                M[X, terminal].append(production)
            if firsts[alpha].contains_epsilon and terminal in follows[X]:
                M[X, terminal].append(production)

            if len(M[X, terminal]) > 1 and (X, terminal) not in _conflict:
                _conflict.append((X, terminal))

        if firsts[alpha].contains_epsilon and G.EOF in follows[X]:
            try:
                _try = M[X, G.EOF]
            except KeyError:
                M[X, G.EOF] = []
            M[X, G.EOF].append(production)
            if len(M[X, G.EOF]) > 1 and (X, G.EOF) not in _conflict:
                _conflict.append((X, G.EOF))
    return M, _conflict


def expand(symbol: Symbol, dic: {}) -> str:
    return dic[symbol]


def sintetize_symbols(G: Grammar):
    dic = {}
    for terminal in G.terminals:
        dic[terminal] = terminal.__str__()

    for i in range(len(G.Productions)):
        for prod in G.Productions:
            try:
                z = dic[prod.Left]
            except KeyError:
                str = ''
                for symbol in prod.Right:
                    try:
                        str += dic[symbol]
                    except:
                        break
                else:
                    dic[prod.Left] = str
    return dic


# X es el no terminal, con c terminal tal q len( M[X,c] ) > 1
def conflict_string(G: Grammar, X: NonTerminal, c: Terminal, M: {}, Firsts, Follows):
    tuples = tuples_road(G, G.startSymbol, X)
    left, right = Get_conflict_production(tuples)
    tuples1 = tuples_road(G, X, c)
    left1, right1 = Get_conflict_production(tuples1)

    _str = ""
    dic = sintetize_symbols(G)

    for elem in right:
        if not elem == X:
            _str += expand(elem, dic)
        else:
            _str += c.__str__()
            for i in range(1, len(right1)):
                _str += expand(right1[i], dic)

    return _str


def tuples_road(G: Grammar, start: Symbol, X: Symbol):
    _used = [start]
    _tuples = []
    next_level = [start]

    while X not in _used:
        aux = []
        for symbol in next_level:
            if symbol.IsNonTerminal:
                for production in symbol.productions:
                    for elem in production.Right:
                        if elem == X:
                            if X.IsNonTerminal or elem == production.Right[0]:
                                _tuples.append((symbol, X))
                                return _tuples
                            else:
                                _tuples.append((symbol, elem))
                                aux.append(elem)
                        elif elem not in _used:
                            _used.append(elem)
                            _tuples.append((symbol, elem))
                            aux.append(elem)

        next_level = aux

    return None


def Get_conflict_production(tuples: []):
    stack = []
    parent = None
    i = len(tuples) - 1
    while i >= 0:
        aux = tuples[i][0]
        if parent is None or aux != parent:
            parent = aux
        else:
            break
        stack.append(tuples[i][1])
        for j in range(i, -1, -1):
            if tuples[j][1] == parent:
                i = j + 1
                break
        i -= 1
    stack.append(tuples[0][0])
    left = tuples[0][0]
    right = tuples[0][0].productions[0].Right
    if len(stack) > 1:
        for production in stack[1].productions:
            a = [x for x in production.Right]
            if a.__contains__(stack[0]):
                left = stack[1]
                right = a
                break

    for i in range(1, len(stack) - 1):
        for production in stack[i + 1].productions:
            a = [x for x in production.Right]
            if a.__contains__(stack[i]):
                b = a.index(stack[i])
                aux0 = [a[i] for i in range(b)]
                aux0.extend(right)
                aux0.extend([a[i] for i in range(b + 1, len(a), 1)])
                right = aux0
                left = stack[i + 1]
                break
    return left, right


G = Grammar()
E = G.NonTerminal('E', True)
T, F, X, Y = G.NonTerminals('T F X Y')
a, b, c = G.Terminals('a b c')

E %= T + X
X %= T + X | G.Epsilon | c + T
T %= F + Y
F %= a + Y | c + Y | G.Epsilon
Y %= b + X | a + T

# E %= X
# E %= T
# X %= T
# X %= Y
# T %= X
# T %= Y
# Y %= a


# firsts = compute_firsts(G)
# follows = compute_follows(G, firsts)
# M, _conflict = build_parsing_table(G, firsts, follows)
# print(conflict_string(G, _conflict[1][0], _conflict[1][1], M, firsts, follows))
