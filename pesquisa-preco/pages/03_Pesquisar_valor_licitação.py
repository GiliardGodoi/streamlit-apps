
import re
import pandas as pd
import requests
import streamlit as st
import time

from bs4 import BeautifulSoup
from io import BytesIO, StringIO
from pathlib import Path
from utils import URL_ABA_PRECOS, URL_TCE_LICITACAO

st.set_page_config(
    page_title="Licitação Pública",
    layout='wide',
    page_icon=""
    )

if not 'data' in st.session_state:
    st.session_state['data'] = None

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

def pesquisar_valor_licitacao(url):

    time.sleep(2)

    response = requests.get(url)
    page = response.content.decode()
    soup = BeautifulSoup(page, 'html.parser')

    dado = dict()

    # Descrição objeto
    e = soup.find(class_='divDadosSimples')
    e = e.find(class_='dados')
    dado['Descrição Licitação'] = e.text

    # Entidade
    e = soup.find(id='tootipClassificacaoJuridica')
    e = e.parent.find(class_='dados')
    dado['Entidade'] = e.text

    # Descrição Modalidade Licitação
    e = soup.find(id='idDsModalidadeLicitacao')
    dado['Procedimento'] = e.text


    # Data Homologação
    e = soup.find(id='idDsTipoSituacaoLicitacao')
    e = e.parent.find(class_='descricao')
    dado['Data Homologacao'] = e.text


    # Valor Licitacao
    e = soup.find(id='idVlLicitacao')
    dado['Valor.Total'] = e.text

    return dado

@st.cache_data(show_spinner='Pesquisando valores...', ttl=360)
def processar_urls_licitacao(urls : list):
    dados = [
        pesquisar_valor_licitacao(url) for url in urls
    ]
    resultado = None
    if dados:
        resultado = pd.DataFrame(dados)

    return resultado


def main():
    st.title("Buscar pelo link")

    container = st.container()

    col1, col2, _ = st.columns([1, 1, 1])

    nro = col2.number_input(
        "Número de links para analisar",
        min_value=1,
        max_value=20,
        value=2,
        step=1,
        label_visibility="collapsed"
        )

    for i in range(nro):
        container.text_input("Link", key=f"in_link_{i}")

    if col1.button("Pesquisar", type="primary", use_container_width=True):
        urls = [st.session_state[f"in_link_{i}"] for i in range(nro)]
        urls = [ url for url in urls if 'TCEPR/Tribunal/Relacon/Licitacao' in url]
        with st.expander(label='Visualizar urls:'):
            st.write(urls)

        df = processar_urls_licitacao(urls)
        st.session_state['data'] = df

    if st.session_state['data'] is not None:
        df = st.data_editor(st.session_state['data'])
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Valores', index=False)

        download_excel = st.download_button(
            label='Download data as Excel',
            data=excel_buffer,
            file_name='valores-licitacao.xlsx',
            mime='application/vnd.ms-excel'
        )




if __name__ == "__main__":
    main()