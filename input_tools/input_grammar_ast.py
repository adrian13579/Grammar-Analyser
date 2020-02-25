from cmp.ast import Node
from cmp.pycompiler import Grammar, Production, Sentence


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
                prod_body = Sentence(context.Terminals[self.right])
            elif self.right in context.NonTerminals:
                prod_body = Sentence(context.NonTerminals[self.right])
        context.Grammar.Add_Production(Production(prod_head, prod_body))
        return