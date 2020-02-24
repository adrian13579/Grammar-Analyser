from cmp.automata import State


def derivation_tree_ll(derivation, index):
    index += 1
    current_production = derivation[index]
    current_state = State(current_production.Left.Name)
    if current_production.Right.IsEpsilon:
        current_state.add_transition('', State('Epsilon'))
    else:
        for symbol in current_production.Right:
            if symbol.IsTerminal:
                current_state.add_transition('', State(symbol.Name))
            else:
                next_state, index = derivation_tree_ll(derivation, index)
                current_state.add_transition('', next_state)
    return current_state, index


def derivation_tree_lr(derivation, index):
    index -= 1
    current_production = derivation[index]
    current_state = State(current_production.Left.Name)
    if current_production.Right.IsEpsilon:
        current_state.add_transition('', State('Epsilon'))
    else:
        for symbol in reversed(current_production.Right):
            if symbol.IsTerminal:
                current_state.add_transition('', State(symbol.Name))
            else:
                next_state, index = derivation_tree_lr(derivation, index)
                current_state.add_transition('', next_state)
    return current_state, index
