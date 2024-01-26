import requests

from bs4 import BeautifulSoup

URL_TCE_SERVICOS = 'https://servicos.tce.pr.gov.br/TCEPR/Tribunal/Relacon/'
URL_TCE_LICITACAO = URL_TCE_SERVICOS + "Licitacao/"
URL_DETALHES_LICITACAO =  URL_TCE_LICITACAO + "LicitacaoDetalhes/Detalhes" # ?IdLicitacao=1982951&IdEntidade=9855&NrAnoLicitacao=2022
URL_ABA_PRECOS = URL_TCE_LICITACAO + "LicitacaoDetalhes/AbaPropostaPrincipal" # ?IdLicitacao=1982951&tipoExibicao=Ajax&Grid-Page=1&Grid-RowsPerPage=100
URL_CONSULTA_LICITACAO = URL_TCE_SERVICOS + "LicitacaoConsulta/Pesquisa"

URL_SAPL = ""

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