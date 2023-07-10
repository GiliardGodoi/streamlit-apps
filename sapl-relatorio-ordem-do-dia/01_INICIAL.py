import streamlit as st
import requests
import json
from collections import defaultdict
from datetime import date
from utils import DOCUMENTO, MATERIA

st.set_page_config(
    page_title="Relatório",
    page_icon=":memo:",
    layout="wide"
)

if 'texto_relatorio' not in st.session_state:
    st.session_state['texto_relatorio'] = False


def get_requests_header():
    url = "https://sapl.santoantoniodaplatina.pr.leg.br/api/auth/token"
    auth_data = {
            'username' : st.secrets['sapl_credentials']['username'],
            'password' : st.secrets['sapl_credentials']['password'],
        }

    response = requests.post(url, data=auth_data)
    if response.status_code == 200 :
        auth = response.json()
        token = auth['token']
        headers={
            'Authorization': f'Token {token}',
            "Content-Type": "application/json"
            }

        return headers
    else:
        raise RuntimeError(
            "Erro na recuperação do token de autenticação",
            f"Resposta do servidor não foi a esperada {response.status_code}"
        )

def main():
    st.header('Relatório de leitura')
    col1, col2 = st.columns(2)
    with col1:
        first = st.date_input("Data Inicial:")
    with col2:
        second = st.date_input("Data Final:")

    days_interval = (second - first).days <= 30

    if not days_interval:
        st.warning("O intervalo entre a data inicial e final está limitado em 30 dias")

    with st.expander("Opções"):
        colA, colB = st.columns(2)
        with colA:
            opt_materias_legislativas = st.checkbox("Matérias Legislativas", value=True)
        with colB:
            opt_markdown = st.checkbox("Markdown", value=False)

    if st.button("Gerar", disabled=(not days_interval)) :
        if first > second :
            st.warning("A data inicial deve ser anterior a data final!")
        else :
            headers = get_requests_header()
            params = {
                'timestamp__gte' : first.strftime("%Y-%m-%d"),
                'timestamp__lte' : second.strftime("%Y-%m-%d"),
            }
            commons = defaultdict(list)
            legislative = defaultdict(list)
            url = "https://sapl.santoantoniodaplatina.pr.leg.br/api/protocoloadm/protocolo?ano=2023"
            pagination = {'links' : {'next' : url}}
            first_time = True

            while pagination['links']['next'] != None:
                url = pagination['links']['next']
                if first_time :
                    response = requests.get(url, headers=headers, params=params)
                    first_time = False
                else:
                    response = requests.get(url, headers=headers)
                content = response.json()
                pagination = content['pagination'] if 'pagination' in content else {'links' : {'next' : None}}
                results = content['results'] if 'results' in content else list()
                docs = [d for d in results if d['ip_anulacao'] == '']

                for doc in docs :
                    if (doc['tipo_materia'] is None) and (doc['tipo_documento'] is not None):
                        commons[doc['tipo_documento']].append(doc)
                    elif (doc['tipo_documento'] is None) and (doc['tipo_materia'] is not None) :
                        legislative[doc['tipo_materia']].append(doc)

        report = list()
        report.append("## Documentos")
        for key, docs in commons.items():
            title = DOCUMENTO[key]['descricao'].upper()
            report.append(f"## {title}")
            for doc in docs:
                report.append(doc['assunto_ementa'])
        
        if opt_materias_legislativas:
            report.append("# Matérias Legislativas")
            for key, docs in legislative.items():
                title = MATERIA[key]['descricao'].upper()
                report.append(f"## {title}")
                for doc in docs:
                    report.append(doc['assunto_ementa'])

        st.session_state['texto_relatorio'] = '\n\n'.join(report)

    if st.session_state['texto_relatorio'] :

        text = st.session_state['texto_relatorio']
        
        if opt_markdown:
            st.write(text)
        else:
            text = st.text_area("Relatório", value=text, height=900, label_visibility='collapsed')
            st.session_state['texto_relatorio'] = text

        st.download_button(
            label="Download",
            data=text,
            file_name='relatorio.txt'
        )

if __name__ == "__main__":
    main()