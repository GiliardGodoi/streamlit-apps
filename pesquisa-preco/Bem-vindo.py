import pandas as pd
import re

import streamlit as st

from utils import raspar_pagina_detalhe_licitacao 

if 'k_links' not in st.session_state:
    st.session_state['k_links'] = 2

# if 'links' not in st.session_state:
#     st.session_state['links'] = []


STRING_PATTERN_LINKS = r'IdLicitacao=(\d+)&IdEntidade=(\d+)&NrAnoLicitacao=(\d+)'

def ui_input_text_links(k, pattern=STRING_PATTERN_LINKS):
    
    def go_up():
        st.session_state['k_links'] = st.session_state.get('k_links', 1) + 1

    def go_down():
        k =  st.session_state.get('k_links', 1) - 1
        if k < 1:
            st.session_state['k_links'] = 1
        else :
            st.session_state['k_links'] = k

    def clear_links():
        st.toast('Ainda não implementado!', icon='😎')

    for i in range(k):
        st.text_input("Link", key=f"link_{i}", label_visibility='collapsed')

    col1, col2, col3, _ = st.columns([0.2, 0.2, 0.2, 0.4])
    with col1:
        st.button('Mais', type='primary', use_container_width=True, on_click=go_up)
    with col2:
        st.button('Menos', type='primary', use_container_width=True, on_click=go_down)
    with col3:
        st.button('Limpar', type='secondary', use_container_width=True, on_click=clear_links)

    links = [st.session_state[f'link_{i}'] for i in range(k) ]
    matches = [ re.search(pattern, link) for link in  links ]

    links = [{
        'link' : link,
        'IdLicitacao': match.group(1),
        'IdEntidade': match.group(2),
        'NrAnoLicitacao': match.group(3),
    } for link, match in zip(links, matches) if match is not None]

    return links


def main():
    st.title('Indicar links')

    links = ui_input_text_links(st.session_state.get('k_links', 1))

    if len(links) > 0:
        with st.expander("Links"):
            st.write(links)
            # col1, col2, col3, _ = st.columns([0.2, 0.2, 0.2, 0.4])
            # with col1:
            #     st.button('Salvar', type='primary', use_container_width=True)
            # with col2:
            #     st.button('Pesquisar', type='secondary', use_container_width=True)
            # with col3:
            #     st.button('Ops', type='secondary', use_container_width=True)

    if len(links) > 0:
        value = st.selectbox("Selecionar", options=links, format_func=lambda d: d['IdLicitacao'])

        if st.button("Pesquisar", type='primary') :
            dado = raspar_pagina_detalhe_licitacao(value['link'])
            dado.update(value)
            st.write(dado)



if __name__ == "__main__":
    main()