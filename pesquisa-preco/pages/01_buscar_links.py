from io import StringIO
import re
import pandas as pd
import requests
import streamlit as st

from pathlib import Path
from utils import URL_ABA_PRECOS, URL_TCE_LICITACAO

st.set_page_config(
    page_title="Licitação Pública",
    layout='wide',
    page_icon=""
    )

if not 'frames' in st.session_state:
    st.session_state.frames = None

def identifica_IdLicitacao(url, pattern=re.compile("IdLicitacao=(\d+)")):
    match = pattern.search(url)
    if match is None:
        return ''
    
    idLicitacao = match.groups()
    if type(idLicitacao) is tuple:
        idLicitacao = idLicitacao[0]

    return idLicitacao

def pesquisar_aba_precos_itens(nroIdLicitacao, nroPagina=1, url=URL_ABA_PRECOS) :

    params = {
        'IdLicitacao' : nroIdLicitacao,
        'tipoExibicao' :'Ajax',
        'Grid-Page'    : nroPagina,
        'Grid-RowsPerPage': 100
    }

    response = requests.get(url, params=params)

    if response.status_code != 200 :
        return None
    content = response.content.decode('utf8')
    dfs = pd.read_html(
        StringIO(content),
        thousands='.',
        decimal=',',
    )

    return dfs

def processar_idLicitacao(ids):
    folder = Path('data', 'precos')
    data = list()
    for idLicitacao in ids:
        df = pesquisar_aba_precos_itens(idLicitacao)[0]
        # df.to_csv(folder / f"{idLicitacao}.csv")
        data.append(df)

    return data
        

def main():
    st.title("Buscar pelo link")

    container = st.container()

    col1, col2, _ = st.columns([1, 1, 1])

    nro = col2.number_input(
        "Número de links para analisar",
        min_value=1,
        max_value=10,
        value=2,
        step=1,
        label_visibility="collapsed"
        )

    for i in range(nro):
        container.text_input("Link", key=f"in_link_{i}")

    if col1.button("Pesquisar", type="primary", use_container_width=True):
        links = [st.session_state[f"in_link_{i}"] for i in range(nro)]
        ids = [identifica_IdLicitacao(url) for url in links if url != '' ]
        st.json(ids)

        with st.spinner():
            frames = processar_idLicitacao(ids)
            st.session_state.frames = frames

    if (st.session_state.frames is not None) and (len(st.session_state.frames) > 0):
        frames = st.session_state.frames
        idx = st.number_input(
            "Ver tabela",
            min_value=1,
            max_value=len(frames)
            )
        idx -= 1 
        # st.write(idx)
        st.dataframe(frames[idx])

if __name__ == "__main__":
    main()