
import pandas as pd
from sqlalchemy import create_engine

from .util import obter_dias_mes
from .util import dias_da_semana

def conectar_com_banco(caminho_db = "sqlite:///registros.db"):
    engine = create_engine(caminho_db, echo=False)

    return engine

def consultar_codigo_pis_no_mes(banco, ano, mes):
    resultado = banco.execute(f"SELECT DISTINCT pis FROM registros WHERE year = {ano} AND month = {mes}").fetchall()
    
    if resultado:
        resultado = [ r[0] for r in resultado]
    else:
        resultado = []

    return resultado

def consultar_nome_servidor(banco, codigo_pis):
    resultado = banco.execute(f"SELECT DISTINCT name FROM funcionarios WHERE pis = '{codigo_pis}'").fetchall()

    nome_servidor = '' # string vazia
    if resultado:
        nome_servidor = resultado[0][0]

    return nome_servidor

def consultar_dados_servidor(banco, codigo_pis, ano, mes):
    query = f"""SELECT * 
            FROM registros 
            WHERE year = {ano} AND month = {mes} AND pis = '{codigo_pis}'
        """

    df = pd.read_sql(query, 
                    banco,
                    parse_dates='datetime')

    df['date'] = df['datetime'].dt.date
    df['rank'] = df.groupby(df.datetime.dt.day)['datetime'].rank().astype(int)

    return df

def processar_registros(frame, ano, mes):
    
    tmp = frame.groupby('date', as_index=True)['rank'].max()
    s1 = (tmp > 0) & (tmp <= 6) & (tmp % 2 == 0)
    s1.name = 'is_valid'

    dias_do_mes = obter_dias_mes(ano, mes)
    tabela = pd.DataFrame(dias_do_mes.day_name(), index=dias_do_mes, columns=['WeekName'])
    tabela['WeekName'] = tabela['WeekName'].map(dias_da_semana)

    frame = frame.drop_duplicates(subset=['date', 'datetime', 'rank'])
    pivoted_df = frame.pivot(index=['date'], columns='rank', values='datetime')
    
    tabela = tabela.merge(
        pivoted_df, 
        right_index=True, left_index=True, how='left'
    )

    tabela = tabela.merge(
        s1,
        right_index=True, left_index=True, how='left'
    )

    tabela['is_valid'] = tabela['is_valid'].fillna(False)

    return tabela


def salvar_relatorio_em_excel(tabela, nome_arquivo, nome_servidor, ano, mes, horario_noturno=False):

    if not isinstance(nome_arquivo, str):
        raise TypeError(f'nome_arquivo should be a string, but got {type(nome_arquivo)}')
    
    if not isinstance(tabela, pd.DataFrame):
        raise TypeError(f'tabela should be a pandas.DataFrame, but got {type(tabela)}')

    writer = pd.ExcelWriter(nome_arquivo,
                        datetime_format='hh:mm',
                        engine='xlsxwriter',)

    planilhas = ['validada', 'original']

    for plan in planilhas:
        # copy the same data in two sheets

        (tabela.reset_index().to_excel(writer, sheet_name=plan, startrow=2, index=False))

        wb = writer.book
        ws = writer.sheets[plan]

        ws.write('A1', 'Servidor:')
        ws.write('B1', nome_servidor)
        ws.write('D1', 'Período:')
        ws.write('E1', f'{mes}/{ano}')

        ws.set_column('A:B', 12)
        # ws.set_column('B:B', 15)
        ws.set_column('C:H', 8)
        ws.set_column('I:I', 15)
        ws.set_column('J:J', 1)
        ws.set_column('K:M', 8)
        ws.set_column('N:N', 2)
        ws.set_column('O:O', 8)
        
        ws.set_column('P:P', 20)
        
        start_cell    = 4
        max_row = len(tabela)
        fmt2 = wb.add_format({'num_format': 'hh:mm:ss'}) # 

        ws.write(f'K{start_cell - 1}', 'Manhã')
        ws.write(f'L{start_cell - 1}', 'Tarde')
        ws.write(f'M{start_cell - 1}', 'Noite')
        ws.write(f'O{start_cell - 1}', 'Total Dia')

        for i in range(0, max_row):
            row = i + start_cell

            cell = f'K{row}'
            formula  = f'=D{row} - C{row}'
            ws.write_formula(cell, formula, fmt2)

            cell = f'L{row}'
            formula  = f'=F{row} - E{row}'
            ws.write_formula(cell, formula, fmt2)

            if horario_noturno:
                cell = f'M{row}'
                formula  = f'=H{row} - G{row}'
                ws.write_formula(cell, formula, fmt2)

            cell = f'O{row}'
            formula = f'K{row} + L{row} + M{row}' if horario_noturno else f'K{row} + L{row}'
            ws.write_formula(cell, formula, fmt2)

    writer.save()

def gerar_nome_arquivo_excel(nome_servidor, ano, mes):
    try:
        nome = nome_servidor.split()[0]
    except :
        nome = 'Não disponível'
    
    return f"{ano} - {mes} - {nome}.xlsx"

def gerar_relatorios(ano, mes):
    
    banco = conectar_com_banco()

    codigos_pis = consultar_codigo_pis_no_mes(banco, ano, mes)

    for codigo in codigos_pis:
        # print(codigo)
        gerar_relatorio_servidor(banco, codigo, ano, mes)

def gerar_relatorio_servidor(banco, codigo_pis, ano, mes):
    
    nome_servidor = consultar_nome_servidor(banco, codigo_pis)
    
    df = consultar_dados_servidor(banco, codigo_pis, ano, mes)

    tabela = processar_registros(df, ano, mes)

    nome_arquivo = gerar_nome_arquivo_excel(nome_servidor, ano, mes)

    salvar_relatorio_em_excel(tabela, nome_arquivo, nome_servidor, ano, mes,
                              horario_noturno = (df['rank'].max() == 6))
