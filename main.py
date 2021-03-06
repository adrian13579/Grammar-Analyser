import copy

import streamlit as st
import pandas as pd

from cmp.automata import lr0_formatter
from cmp.derivation_tree import derivation_tree_ll, derivation_tree_lr
from cmp.first_follow import compute_firsts, compute_follows
from cmp.grammar import eliminate_left_recursion, remove_common_prefix, remove_useless_non_terminals, \
    remove_unreachable_symbols
from cmp.lalr_parser import LALR1Parser, build_LALR1_automaton, conflict_string_lalr
from cmp.ll1_parser import build_parsing_table, metodo_predictivo_no_recursivo, conflict_string, \
    deprecated_metodo_predictivo_no_recursivo
from cmp.lr1_parser import build_LR1_automaton, LR1Parser, conflict_string_lr1
from cmp.regular_grammar import reg_grammar_to_automaton, State, automaton_to_reg_expression
from cmp.slr1_parser import SLR1Parser, build_LR0_automaton, conflict_string_slr1
from input_tools.input_parser import Input

input_grammar_example = '''
Distinguido: E
NoTerminales: T, F
Terminales: plus, star, num, paro,parc
E = E + plus + T
E = T
T = T + star + F
T = F
F = num
F = paro + E + parc
'''
# A = a + A
# A = epsilon
# B = b + B
# B = epsilon
# C = c + C
# C = epsilon
# '''

input_regex_example = '''
num  :  num ,
plus :  +,
star :  @,
paro : [,
parc: ]
'''
G = None
parser = None
string = 'num+num@num'
input = None
parsing_table = None
_conflict = []
GG = None
goto = None
action = None


def table_to_dataframe(m):
    return pd.DataFrame.from_dict(m, orient='index', dtype=str)


if __name__ == '__main__':
    st.title('Grammar Analyser')
    st.sidebar.title('Set Output')

    input_grammar = st.text_area('Grammar', input_grammar_example)
    input_regex = st.text_area('Regex', input_regex_example)

    string = st.text_input('String', string)
    start = st.button('Start')

    derivation_tree_select = st.sidebar.checkbox('Derivation Tree')
    eliminate_left_recursion_select = st.sidebar.checkbox('Eliminate Left Recursion')
    remove_unnecesary_productions_select = st.sidebar.checkbox('Remove Useless Production')
    remove_common_prefix_select = st.sidebar.checkbox('Remove Common Prefix')
    reg_grammar_to_automaton_select = st.sidebar.checkbox('Regular Grammar to Automaton')
    regular_grammar_to_reg_expression_select = st.sidebar.checkbox('Regular Grammar to Regular Expression')
    parsing_table_select = st.sidebar.checkbox('Parsing Table')
    # start = True
    # derivation_tree_select = True
    parser_type = st.sidebar.selectbox(label='Parser', options=('ll(1)', 'lr(1)', 'slr(1)', 'lalr'))
    # parser_type = 'slr(1)'
    st.sidebar.markdown('''#### Produced by:  
       Adrian Rodriguez Portales
       Osmany Perez ''')
    if input_grammar != '' and input_regex != '' and string != '':
        # try:
        input_error = False
        try:
            input = Input(input_grammar, input_regex)
            G = input.get_grammar()
            GG =G.AugmentedGrammar()
        except:
            input_error = True
            st.warning('Wrong input format or some terminals are undefined')

        if not input_error:
            if parser_type == 'll(1)':
                firsts = compute_firsts(G)
                follows = compute_follows(G, firsts)
                parsing_table, _conflict = build_parsing_table(G, firsts, follows)
                parser = deprecated_metodo_predictivo_no_recursivo(G, parsing_table)
                if len(_conflict) != 0:
                    _conflict = conflict_string(G, _conflict[0][0], _conflict[0][1], parsing_table, firsts, follows)

            if parser_type == 'slr(1)':
                parser = SLR1Parser(G, verbose=True)
                _str = conflict_string_slr1(parser.action, parser.goto, GG.terminals + [GG.EOF])
                if _str is not None:
                    _conflict = _str

            if parser_type == 'lr(1)':
                parser = LR1Parser(G, verbose=True)
                _str = conflict_string_lr1(parser.action, parser.goto, GG.terminals + [GG.EOF])
                if _str is not None:
                    _conflict = _str

            if parser_type == 'lalr':
                parser = LALR1Parser(G)
                _str = conflict_string_lalr(parser.action, parser.goto, GG.terminals + [GG.EOF])
                if _str is not None:
                    _conflict = _str
            if start:
                if remove_unnecesary_productions_select:
                    remove_useless_non_terminals(G)
                    # st.header('Remove useless non-terminals:')
                    # st.text(str(G))
                    st.header('Remove unreachable symbols:')
                    remove_unreachable_symbols(G)
                    st.text(str(G))

                if eliminate_left_recursion_select:
                    eliminate_left_recursion(G)
                    st.header('Eliminate left recursion:')
                    st.text(str(G))

                if remove_common_prefix_select:
                    remove_common_prefix(G)
                    st.header('Remove common prefix:')
                    st.text(str(G))

                if reg_grammar_to_automaton_select:
                    G_copy = copy.deepcopy(G)
                    automaton = reg_grammar_to_automaton(G_copy)
                    # st.text(str(automaton.transitions))
                    if automaton is not None:
                        automaton = State.from_nfa(automaton)
                        st.header('Automata from regular grammar:')
                        st.graphviz_chart(str(automaton.graph()))
                        st.text(str(automaton.transitions))
                    else:
                        st.text("The grammar is not regular.")

                if parsing_table_select:
                    st.header('Parsing table')
                    if parser_type != 'll(1)':
                        st.dataframe(table_to_dataframe(parser.goto))
                        st.dataframe(table_to_dataframe(parser.action))
                    else:
                        st.dataframe(table_to_dataframe(parsing_table))

                if regular_grammar_to_reg_expression_select:
                    G_copy = copy.deepcopy(G)
                    automaton = reg_grammar_to_automaton(G_copy)
                    if automaton is not None:
                        regex = automaton_to_reg_expression(automaton)
                        st.text(regex)
                    else:
                        st.text("The grammar is not regular.")

                if derivation_tree_select:
                    st.text(_conflict)
                    if len(_conflict) != 0:
                        st.warning('This string generates conflicts!')

                    else:
                        if parser_type == 'slr(1)':
                            automaton = build_LR0_automaton(GG)
                            automaton = automaton.to_deterministic(lr0_formatter)
                            st.header('Automaton lr(0)')
                            st.graphviz_chart(str(automaton.graph()))
                        elif parser_type == 'lr(1)':
                            automaton = build_LR1_automaton(GG)
                            st.header('Automaton lr(1)')
                            st.graphviz_chart(str(automaton.graph()))
                        elif parser_type == 'lalr':
                            automaton = build_LALR1_automaton(GG)
                            st.header('Automaton lalr')
                            st.graphviz_chart(str(automaton.graph()))

                        try:
                            tokens = input.tokenize_input_string(string)
                            derivation = parser([token.token_type for token in tokens])
                            tree, _ = derivation_tree_ll(derivation,
                                                         -1) if parser_type == 'll(1)' else derivation_tree_lr(
                                derivation,
                                len(
                                    derivation))
                            st.header('Derivation Tree:')
                            st.graphviz_chart(str(tree.graph()))
                        except:
                            st.warning('String cannot be parsed.')

    # except:
    #     st.warning("Oops, there's something wrong XD")
