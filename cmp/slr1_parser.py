from cmp.automata import State
from cmp.pycompiler import Item
from cmp.first_follow import compute_firsts, compute_follows
from cmp.shift_reduce_parser import ShiftReduceParser


def build_LR0_automaton(G):
    assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'

    start_production = G.startSymbol.productions[0]
    start_item = Item(start_production, 0)

    automaton = State(start_item, True)

    pending = [start_item]
    visited = {start_item: automaton}

    while pending:
        current_item = pending.pop()
        if current_item.IsReduceItem:
            continue

        # Your code here!!! (Decide which transitions to add)
        new_item = current_item.NextItem()
        transition_symbol = current_item.NextSymbol.Name
        next_items = [(new_item, transition_symbol)]

        if current_item.NextSymbol in G.nonTerminals:
            for production in current_item.NextSymbol.productions:
                new_item = Item(production, 0)
                next_items.append((new_item, G.Epsilon))

        current_state = visited[current_item]
        # Your code here!!! (Add the decided transitions)
        for item, symbol in next_items:
            try:
                state = visited[item]
            except KeyError:
                state = State(item, True)
                visited[item] = state
                pending.append(item)

            if symbol == G.Epsilon:
                current_state.add_epsilon_transition(state)
            else:
                current_state.add_transition(symbol, state)

    return automaton


class SLR1Parser(ShiftReduceParser):

    def _build_parsing_table(self):
        G = self.G.AugmentedGrammar(True)
        firsts = compute_firsts(G)
        follows = compute_follows(G, firsts)

        automaton = build_LR0_automaton(G).to_deterministic()
        for i, node in enumerate(automaton):
            if self.verbose:
                print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i

        for node in automaton:
            idx = node.idx
            for state in node.state:
                item = state.state
                # Your code here!!!
                # - Fill `self.Action` and `self.Goto` according to `item`)
                # - Feel free to use `self._register(...)`)
                if item.IsReduceItem and item.production.Left == G.startSymbol:
                    self._register(self.action, (idx, G.EOF), (self.OK, 0))
                elif item.IsReduceItem:
                    for symbol in follows[item.production.Left]:
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