import pandas as pd
import re
import requests
import streamlit as st

from bs4 import BeautifulSoup
from io import StringIO

from utils import URL_ABA_PRECOS

if 'k_links' not in st.session_state:
    st.session_state['k_links'] = 2

if 'licitacao' not in st.session_state:
    st.session_state['licitacao'] = None

st.set_page_config(
    page_title="Buscar por links",
    layout='wide'
)

STRING_PATTERN_LINKS = r'IdLicitacao=(\d+)&IdEntidade=(\d+)&NrAnoLicitacao=(\d+)'

def clean_selection_detalhes_licitacao():
    st.session_state['licitacao'] = None


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
        'seq' : i,
        'link' : link,
        'IdLicitacao': match.group(1),
        'IdEntidade': match.group(2),
        'NrAnoLicitacao': match.group(3),
    } for i, (link, match) in enumerate(zip(links, matches), start=1) if match is not None]

    return links

@st.cache_data(show_spinner="Pesquisando detalhes da licitação...")
def raspar_pagina_detalhe_licitacao(url):
    '''
    '''
    response = requests.get(url)
    page = response.content.decode()
    soup = BeautifulSoup(page, 'html.parser')

    dado = dict()

    # Número da Licitação
    e = soup.find(id="idNrLicitacao")
    dado['idNrLicitacao'] = e.text

    # Descrição objeto
    e = soup.find(class_='divDadosSimples')
    e = e.find(class_='dados')
    dado['Descrição.Licitação'] = e.text

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
    dado['Data.Homologacao'] = e.text


    # Valor Licitacao
    e = soup.find(id='idVlLicitacao')
    dado['Valor.Total'] = e.text

    return dado

@st.cache_data(show_spinner="Pesquisando preços...")
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

def main():
    st.header('Indicar links', divider=True)
    '''Pesquisa ao painel de licitações do [Portal Informação para Todos do TCE-PR](https://servicos.tce.pr.gov.br/TCEPR/Tribunal/Relacon/Licitacao)
    '''

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
        st.header('Pesquisar licitação', divider=True)
        selected = st.selectbox("Selecionar",
                             options=links,
                             format_func=lambda d: f"Seq: {d['seq']} - IdLicitação: {d['IdLicitacao']}",
                             on_change=clean_selection_detalhes_licitacao)


        if st.button("Pesquisar", type='primary') :
            detalhe_licitacao = raspar_pagina_detalhe_licitacao(selected['link'])
            tabelas  = pesquisar_aba_precos_itens(selected['IdLicitacao'])
            tabela_preco = tabelas[0] if len(tabelas) > 0 else None
            tabela_preco.insert(0, 'Considerar', True)
            detalhe_licitacao.update(selected)
            st.session_state['licitacao'] = {
                'detalhe_licitacao' : detalhe_licitacao,
                'tabela_preco' : tabela_preco
            }

    if st.session_state['licitacao'] is not None:
        # st.header('Selecionar itens', divider=True)
        licitacao = st.session_state['licitacao']
        st.write(licitacao['detalhe_licitacao'])
        columns = st.multiselect('Visualizar colunas:',
                                 options=licitacao['tabela_preco'].columns,
                                 default=['Considerar', 'Descrição', 'Unidade',
                                          'Quantidade.1', 'Valor', 'Total (R$)',
                                          'Classificação', 'Participante'])
        precos_selecionados = st.data_editor(licitacao['tabela_preco'],
                                             column_order=columns,
                                             use_container_width=True)



if __name__ == "__main__":
    main()