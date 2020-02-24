import streamlit as st

from input_tools.input_parser import Input

if __name__ == '__main__':
    st.title('Grammar Analyser')
    st.sidebar.checkbox('dnivdn')
    st.sidebar.title('Set Grammar')
    st.sidebar.text_area('Grammar',
                         '''
Distinguido: S
NoTerminales: A, B, C
Terminales: a,b,c
S = A + B + C
    ''')
    st.sidebar.text_area('Regex','''
a : (a)*,
b : (b)*,
c : (c|C)*
''')
    st.sidebar.selectbox(label='Parser', options=('ll(1)', 'lr(1)', 'slr(1)', 'lalr(1)'))

    st.sidebar.markdown('''### Produced by:  
    Adrian Rodriguez Portales
    Osmany Perez Yegua''')

    st.text_input('String')
