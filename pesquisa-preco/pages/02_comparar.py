import pandas as pd
import streamlit as st

dfs = pd.read_html('https://servicos.tce.pr.gov.br/TCEPR/Tribunal/Relacon/Licitacao/LicitacaoDetalhes/AbaPropostaPrincipal?IdLicitacao=2077430&tipoExibicao=Ajax&Grid-Page=1&Grid-RowsPerPage=100')

st.dataframe(dfs[0])