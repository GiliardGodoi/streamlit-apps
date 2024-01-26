import streamlit as st
import re
import requests
import pandas as pd

from bs4 import BeautifulSoup
from datetime import date, timedelta
from io import StringIO
from pathlib import Path

from utils import URL_CONSULTA_LICITACAO

if 'frames' not in st.session_state:
    st.session_state.frames = None

if 'dataframe' not in st.session_state:
    st.session_state.dataframe = None

st.set_page_config(
    page_title="Licitação Pública",
    layout='wide',
    page_icon=""
    )

def ui_formulario_consulta():
    today = date.today()
    one_year_ago = today - timedelta(days=365)
    with st.form(key="FormConsultaLicitacao"):
        col1, col2 = st.columns([1, 1])
        with col1 :
            st.selectbox(
                "Natureza Jurídica",
                [
                    ("39", "Poder Legislativo (Câmara Municipal)" ),
                    ("38" , "Poder Executivo Municipal")
                ],
                format_func=lambda x : x[1],
                key="NaturezaJuridica_idNaturezaJuridica"
                )
            st.selectbox(
                "Modalidade",
                [
                    ("0", "Todas"),
                    ("1", "Convite"),
                    ("2", "Tomada de Preço"),
                    ("3", "Concorrência"),
                    ("4", "Concurso"),
                    ("5", "Leilão"),
                    ("6", "Pregão"),
                    ("7", "Processo Dispensa"),
                    ("8", "Processo Inexigibilidade"),
                    ("9", "RDC"),
                    ("10", "Lei Ordinária 13.303/2016"),
                    ("11", "Diálogo Competitivo")
                ],
                format_func=lambda x : x[1],
                key='idModalidadeLicitacao'
            )
            st.write("Data de abertura:")
            col_init, col_end = st.columns([1, 1])
            col_init.date_input("Início:", key="dataAbertura", value=one_year_ago, format="DD/MM/YYYY")
            col_end.date_input("Fim:", key='dataAberturaAte', value=today, format="DD/MM/YYYY")

        with col2:
            st.text_input("Município", disabled=True, label_visibility='hidden', key=1)
            st.multiselect(
                "Situação Licitação:", 
                [
                    (1, 'Andamento'),
                    (7, 'Andamento - Nova Data de Abertura'),
                    (6, 'Homologada'),
                    (2, 'Anulado'),
                    (3, 'Revogada'),
                    (4, 'Deserta'),
                    (5, 'Fracassada'),
                ],
                format_func=lambda x : x[1],
                default=None,
                key='idsSituacao')
            st.write("Data do Edital:")
            col_init, col_end = st.columns([1, 1])
            col_init.date_input("Início:", key='dataEdital', value=one_year_ago, format="DD/MM/YYYY")
            col_end.date_input("Fim:", key='dataEditalAte', value=today, format="DD/MM/YYYY")

        st.text_input("Descrição do objeto:", key='objeto')
        st.text_input("Participante:", key='participante')

        submeter = st.form_submit_button("Pesquisar")

    if submeter :
        with st.spinner('Consultando...'):
            resposta = submeter_consulta()
        if resposta.status_code == 200:
            df = recuperar_tabela(resposta)
            st.session_state.dataframe = df
        else :
            st.warning(f"Requisição retornou {resposta.status_code=}")

def submeter_consulta():
    params = parametros_consulta()
    # st.json(params)
    resposta = requests.post(URL_CONSULTA_LICITACAO, data=params)

    return resposta

def parametros_consulta() -> dict:
    '''
    idsSituacao: 
        1 : Andamento
        7 : Andamento - Nova Data de Abertura
        6 : Homologada
        2 : Anulado
        3 : Revogada
        4 : Deserta
        5 : Fracassada
    idModalidadeLicitacao
        1 : Convite
        2 : Tomada de Preço
        3 : Concorrência
        4 : Concurso
        5 : Leilão
        6 : Pregão
        7 : Processo Dispensa
        8 : Processo Inexigibilidade
        9 : RDC
        10 : Lei Ordinária 13.303/2016
        11 : Diálogo Competitivo
    '''
    # Valores padrão
    params = {
        # "Esfera_idEsfera" : "0",
        # "EstruturaAdministracao_idEstruturaDeAdministracao" :  "0",
        # "Municipio_idMunicipio" :  "0",
        # "NaturezaJuridica_idNaturezaJuridica" :  "38",
        "comissao" :  "",
        "dataAbertura" :  "",
        "dataAberturaAte" :  "", # '%Y-%m-%dT%H:%M:%S.%fZ'
        "dataEdital" :  "",  # "2022-04-01T00:00:00"
        "dataEditalAte" : "", # "2023-04-15T00:00:00"
        "flFiltroExecutado" : False,
        "idAvaliacaoLicitacao" : "0",
        "idClassificacaoObjetoLicitacao" : "0",
        "idEsfera" : "0",
        "idEstruturaDeAdministracao" : "0",
        "idModalidadeLicitacao" : "0",
        "idMunicipio" : "0",
        "idNaturezaJuridica" : "38",
        "idRegimeExecucaoLicitacao" : "0",
        "idsSituacao" : "",
        "moneyRangeMax" : "",
        "moneyRangeMin" : "",
        "nrAno" : "-1",
        "nrOrdem" : 0,
        "nrPagina" : 1,
        "nrRegPorPagina" : 100,
        "numero" : "",
        "objeto" : "",
        "participantes" : "",
        "valorAte" : None,
        "valorEntre" : None,
    }

    params['idNaturezaJuridica'] = st.session_state['NaturezaJuridica_idNaturezaJuridica'][0]
    params['idModalidadeLicitacao'] = st.session_state['idModalidadeLicitacao'][0]
    params['dataAbertura'] = st.session_state['dataAbertura'].strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    params['dataAberturaAte'] = st.session_state['dataAberturaAte'].strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    params['dataEdital'] = st.session_state['dataEdital'].strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    params['dataEditalAte'] = st.session_state['dataEditalAte'].strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    params['objeto'] = st.session_state['objeto']
    params['participante'] = st.session_state['participante']

    params['idsSituacao'] = ','.join([ str(v[0]) for v in sorted(st.session_state['idsSituacao'])])

    return params

def identificar_quantidade_registros(resposta):
    soup = BeautifulSoup(resposta.content.decode('utf-8'))
    selection = soup.select_one('span.infoRodape')
    if selection is None:
        return -1
    text = selection.text.lower()
    m = re.search("total de licitações (\d+)", text)
    if m is None:
        return 0
    
    number  = m.groups()[0]
    return int(number)

def recuperar_tabela(resposta) -> pd.DataFrame :
    content = resposta.content.decode('utf-8')
    tables = pd.read_html(StringIO(content),
                          thousands='.',
                          decimal=',',
                          encoding='utf-8',
                          extract_links='body'
                          )
    
    assert type(tables) == list and len(tables) == 1

    df = tables[0]
    
    links = df.iloc[:, -1].apply(lambda t: t[1] if type(t) == tuple else t)

    df = (df
        .iloc[:, :-1]
        .map(lambda t: t[0] if type(t) == tuple else t)
        .assign(linkLicitacao=links)
        .assign(IdLicitacao=links.str.extract(r'IdLicitacao=(\d+)'))
        .assign(IdEntidade=links.str.extract(r'IdEntidade=(\d+)'))
        .assign(NrAnoLicitacao=links.str.extract(r'NrAnoLicitacao=(\d+)'))
    )
    df.insert(0, 'Considerar', True)

    return df

def ui_show_dataframe(df):
    
    rdf = st.data_editor(df, use_container_width=True)
    st.write(rdf)

def main():
    st.title("Buscar Licitação")

    ui_formulario_consulta()

    if st.session_state.dataframe is not None:
        ui_show_dataframe(st.session_state.dataframe)

if __name__ == "__main__":
    main()
    