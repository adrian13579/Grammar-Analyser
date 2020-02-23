from automata import nfa_to_dfa, automata_minimization
from cmp.ast import Node
from cmp.pycompiler import Grammar, Terminal
from first_follow import compute_follows, compute_firsts
from lexer import Lexer
from ll1_parser import metodo_predictivo_no_recursivo, build_parsing_table
from regular_expression import evaluate_parse

G = Grammar()
S = G.NonTerminal('S', True)
D, N, NA, T, TA, R, Q, O, Z = G.NonTerminals('D N NA T TA R Q O Z')
dist, non_terminal, terminal, points, _id, comma, equal, plus, epsilon = G.Terminals(
    'Distinguido NoTerminal Terminal : id , = + ε')

S %= D + N + T + Q + R
D %= dist + points + _id

N %= non_terminal + points + _id + NA
NA %= comma + _id + NA
NA %= G.Epsilon

T %= terminal + points + _id + TA
TA %= comma + _id + TA
TA %= G.Epsilon

R %= Q + R
R %= G.Epsilon

Q %= _id + equal + O
O %= _id + Z
Z %= plus + _id + Z
Z %= G.Epsilon

nonzero_digits = '|'.join(str(n) for n in range(1, 10))
letters = '|'.join(chr(n) for n in range(ord('a'), ord('z') + 1))
upper_letters = '|'.join(chr(n) for n in range(ord('A'), ord('Z')))

lexer = Lexer([
    (dist, 'Distinguido'),
    (terminal, 'Terminales'),
    (non_terminal, 'NoTerminales'),
    (comma, ','),
    (equal, '='),
    (plus, '+'),
    (points, ':'),
    ('salto', '\n'),
    ('space', ' *'),
    (_id, f'({letters}|{upper_letters})*')
], G.EOF
)


class Context:
    def __init__(self):
        self.Grammar = Grammar()
        self.Terminals = {}
        self.NTerminals = {}
        self.Productions = {}


class GrammarNode(Node):
    def __init__(self, lis):
        self.lis = lis

    def evaluate(self, context: Context):
        for i in self.lis:
            i.evaluate(context)
        return context.Grammar

class TerminalNode(Node):
    def __init__(self,terminal:Terminal):



tokens = lexer('''
Distinguido: S
NoTerminales: A, B, C
Terminales: a, b, c
S = A + B + C
A = a + A
B = b + B
C = c + C
''')

print(tokens)
tokens = [x for x in tokens if
          x.token_type not in ('space', 'salto')]

print(tokens)
# lexer.automaton.graph().write_png('a.png')
first = compute_firsts(G)
follow = compute_follows(G, first)
parsing_table = build_parsing_table(G, first, follow)
parser = metodo_predictivo_no_recursivo(G, parsing_table)
left_parse = parser(tokens)
print(left_parse)
# ast = evaluate_parse(left_parse, tokens)
# nfa = ast.evaluate()
# dfa = nfa_to_dfa(nfa)
# mini = automata_minimization(dfa)

print(12)
