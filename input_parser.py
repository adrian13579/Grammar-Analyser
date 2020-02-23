from automata import nfa_to_dfa, automata_minimization
from cmp.ast import Node
from cmp.pycompiler import Grammar, Terminal, Production
from first_follow import compute_follows, compute_firsts
from lexer import Lexer
from ll1_parser import metodo_predictivo_no_recursivo, build_parsing_table
from regular_expression import evaluate_parse

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


class Context:
    def __init__(self):
        self.NonTerminals = {}
        self.Grammar = Grammar()
        self.Terminals = {}
        self.Productions = {}


class GrammarNode(Node):
    def __init__(self, lis):
        self.lis = lis

    def evaluate(self, context: Context):
        for i in self.lis:
            i.evaluate(context)
        return


class DistNode(Node):
    def __init__(self, dist_id):
        self.dist_id = dist_id

    def evaluate(self, context: Context):
        context.NonTerminals[self.dist_id] = context.Grammar.NonTerminal(self.dist_id, True)


class TerminalNode(Node):
    def __init__(self, terminal_id):
        self.terminal_id = terminal_id

    def evaluate(self, context: Context):
        context.Terminals[self.terminal_id] = context.Grammar.Terminal(self.terminal_id)
        return


class NonTerminalNode(Node):
    def __init__(self, non_terimnal_id):
        self.non_terminal_id = non_terimnal_id

    def evaluate(self, context: Context):
        context.NonTerminals[self.non_terminal_id] = context.Grammar.NonTerminal(self.non_terminal_id)
        return


class EpsilonNode(Node):
    def __init__(self):
        pass

    def evaluate(self, context: Context):
        return


class SentenceNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, context: Context):
        b = context.Terminals[str(self.right)] if str(self.right) in context.Terminals else context.NonTerminals[
            str(self.right)]
        if not isinstance(self.left, SentenceNode):
            a = context.Terminals[str(self.left)] if str(self.left) in context.Terminals else context.NonTerminals[
                str(self.left)]
            return a + b
        temp = self.left.evaluate(context)
        return temp + b


class ProductionNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, context: Context):
        prod_head = context.NonTerminals[self.left]
        prod_body = context.Grammar.Epsilon
        if isinstance(self.right, SentenceNode):
            prod_body = self.right.evaluate(context)
        else:
            if self.right in context.Terminals:
                prod_body = context.Terminals[self.right]
            elif self.right in context.NonTerminals:
                prod_body = context.NonTerminals[self.right]
        context.Grammar.Add_Production(Production(prod_head, prod_body))
        return


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

input_regex = '''
a : (a)*,
b : (b)*,
c : (c|C)*
'''

string = 'aaaaaabbbbcCCCcc'

var = Input(input_gram, input_regex)
print(var.get_grammar())
print(var.tokenize_input_string(string))
