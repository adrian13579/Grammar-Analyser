# from pandas import DataFrame

from cmp.automata import State, multiline_formatter
from cmp.pycompiler import Item
from cmp.utils import ContainerSet
from cmp.first_follow import compute_local_first, compute_firsts
from cmp.shift_reduce_parser import ShiftReduceParser


def expand(item, firsts):
    next_symbol = item.NextSymbol
    if next_symbol is None or not next_symbol.IsNonTerminal:
        return []

    lookaheads = ContainerSet()
    # Your code here!!! (Compute lookahead for child items)
    for preview in item.Preview():
        lookaheads.hard_update(compute_local_first(firsts, preview))

    assert not lookaheads.contains_epsilon
    # Your code here!!! (Build and return child items)
    items = []
    for production in next_symbol.productions:
        items.append(Item(production, 0, lookaheads))
    return items


def compress(items):
    centers = {}

    for item in items:
        center = item.Center()
        try:
            lookaheads = centers[center]
        except KeyError:
            centers[center] = lookaheads = set()
        lookaheads.update(item.lookaheads)

    return {Item(x.production, x.pos, set(lookahead)) for x, lookahead in centers.items()}


def closure_lr1(items, firsts):
    closure = ContainerSet(*items)

    changed = True
    while changed:
        changed = False

        new_items = ContainerSet()
        # Your code here!!!
        for item in closure:
            new_items.extend(expand(item, firsts))

        changed = closure.update(new_items)

    return compress(closure)


def goto_lr1(items, symbol, firsts=None, just_kernel=False):
    assert just_kernel or firsts is not None, '`firsts` must be provided if `just_kernel=False`'
    items = frozenset(item.NextItem() for item in items if item.NextSymbol == symbol)
    return items if just_kernel else closure_lr1(items, firsts)


def build_LR1_automaton(G):
    assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'

    firsts = compute_firsts(G)
    firsts[G.EOF] = ContainerSet(G.EOF)

    start_production = G.startSymbol.productions[0]
    start_item = Item(start_production, 0, lookaheads=(G.EOF,))
    start = frozenset([start_item])

    closure = closure_lr1(start, firsts)
    automaton = State(frozenset(closure), True)

    pending = [start]
    visited = {start: automaton}

    while pending:
        current = pending.pop()
        current_state = visited[current]

        for symbol in G.terminals + G.nonTerminals:
            # Your code here!!! (Get/Build `next_state`)
            closure = closure_lr1(current, firsts)
            goto = goto_lr1(closure, symbol, firsts, True)

            if not goto:
                continue
            try:
                next_state = visited[goto]
            except KeyError:
                closure = closure_lr1(goto, firsts)
                next_state = visited[goto] = State(frozenset(closure), True)
                pending.append(goto)

            current_state.add_transition(symbol.Name, next_state)

    automaton.set_formatter(multiline_formatter)
    return automaton


class LR1Parser(ShiftReduceParser):
    def _build_parsing_table(self):
        G = self.G.AugmentedGrammar(True)

        automaton = build_LR1_automaton(G)
        for i, node in enumerate(automaton):
            if self.verbose: print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i

        for node in automaton:
            idx = node.idx
            for item in node.state:
                # Your code here!!!
                # - Fill `self.Action` and `self.Goto` according to `item`)
                # - Feel free to use `self._register(...)`)
                if item.IsReduceItem and item.production.Left == G.startSymbol:
                    self._register(self.action, (idx, G.EOF), (self.OK, 0))
                elif item.IsReduceItem:
                    for symbol in item.lookaheads:
                        self._register(self.action, (idx, symbol), (self.REDUCE, item.production))
                elif item.NextSymbol.IsTerminal:
                    next_idx = node.transitions[item.NextSymbol.Name][0].idx
                    self._register(self.action, (idx, item.NextSymbol), (self.SHIFT, next_idx))
                elif item.NextSymbol.IsNonTerminal:
                    next_idx = node.transitions[item.NextSymbol.Name][0].idx
                    self._register(self.goto, (idx, item.NextSymbol), next_idx)

    @staticmethod
    def _register(table, key, value):
        assert key not in table or table[key] == value, 'Shift-Reduce or Reduce-Reduce conflict!!!'
        table[key] = value


# def encode_value(value):
#     try:
#         action, tag = value
#         if action == ShiftReduceParser.SHIFT:
#             return 'S' + str(tag)
#         elif action == ShiftReduceParser.REDUCE:
#             return repr(tag)
#         elif action == ShiftReduceParser.OK:
#             return action
#         else:
#             return value
#     except TypeError:
#         return value


# def table_to_dataframe(table):
#     d = {}
#     for (state, symbol), value in table.items():
#         value = encode_value(value)
#         try:
#             d[state][symbol] = value
#         except KeyError:
#             d[state] = {symbol: value}
#
#     return DataFrame.from_dict(d, orient='index', dtype=str)
