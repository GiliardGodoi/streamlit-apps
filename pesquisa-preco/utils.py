import requests

from bs4 import BeautifulSoup

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