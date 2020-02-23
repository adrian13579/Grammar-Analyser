from cmp.ast import Node
from cmp.pycompiler import Grammar, Production
from cmp.first_follow import compute_follows, compute_firsts
from cmp.lexer import Lexer
from cmp.ll1_parser import metodo_predictivo_no_recursivo, build_parsing_table
from cmp.regular_expression import evaluate_parse
from input_tools.input_grammar_ast import GrammarNode, DistNode, EpsilonNode, NonTerminalNode, TerminalNode, \
    ProductionNode, SentenceNode, Context

G = Grammar()
S = G.NonTerminal('S', True)
D, N, NA, T, TA, R, Q, O, Z = G.NonTerminals('D N NA T TA R Q O Z')
dist, non_terminal, terminal, points, _id, comma, equal, plus, epsilon = G.Terminals(
    'Distinguido NoTerminal Terminal : id , = + ε')

S %= D + N + T + Q + R, lambda h, s: GrammarNode([s[1], s[2], s[3], s[4], s[5]])
D %= dist + points + _id, lambda h, s: DistNode(s[3])

N %= non_terminal + points + _id + NA, lambda h, s: GrammarNode([NonTerminalNode(s[3]), s[4]]),
NA %= comma + _id + NA, lambda h, s: GrammarNode([NonTerminalNode(s[2]), s[3]])
NA %= G.Epsilon, lambda h, s: EpsilonNode()

T %= terminal + points + _id + TA, lambda h, s: GrammarNode([TerminalNode(s[3]), s[4]])
TA %= comma + _id + TA, lambda h, s: GrammarNode([TerminalNode(s[2]), s[3]])
TA %= G.Epsilon, lambda h, s: EpsilonNode()

R %= Q + R, lambda h, s: GrammarNode([s[1], s[2]])
R %= G.Epsilon, lambda h, s: EpsilonNode()

Q %= _id + equal + O, lambda h, s: ProductionNode(s[1], s[3])
O %= _id + Z, lambda h, s: s[2], None, lambda h, s: s[1]
Z %= plus + _id + Z, lambda h, s: s[3], None, None, lambda h, s: SentenceNode(h[0], s[2])
Z %= G.Epsilon, lambda h, s: h[0]

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


class Input:
    def __init__(self, input_grammar: str, input_regex: str):
        first = compute_firsts(G)
        follow = compute_follows(G, first)
        parsing_table = build_parsing_table(G, first, follow)
        parser = metodo_predictivo_no_recursivo(G, parsing_table)
        tokens = lexer(input_grammar)
        tokens = [x for x in tokens if
                  x.token_type not in ('space', 'salto')]
        left_parse = parser(tokens)
        self.context = Context()
        ast = evaluate_parse(left_parse, tokens)
        ast.evaluate(self.context)

        regex_str = ''
        for i in input_regex:
            if i not in (' ', '\n'):
                regex_str += i
        regex_str = regex_str.split(',')
        regex = []
        for i in regex_str:
            print(i)
            type, lex = i.split(':')
            type = type.strip()
            lex = lex.strip()
            try:
                regex.append((self.context.Grammar.symbDict[type], lex))
            except KeyError:
                raise Exception('Undefined Expression')

        self.lexer = Lexer(regex, self.context.Grammar.EOF)

    def get_grammar(self):
        return self.context.Grammar

    def tokenize_input_string(self, string: str):
        return self.lexer(string)


input_gram = '''
Distinguido: S
NoTerminales: A, B, C
Terminales: a, b, c
S = A + B + C
A = epsilon
'''

input_rege = '''
a : (a)*,
b : (b)*,
c : (c|C)*
'''

string = 'aaaaaabbbbcCCCcc'

var = Input(input_gram, input_rege)
print(var.get_grammar())
print(var.tokenize_input_string(string))
