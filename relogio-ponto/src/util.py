import pandas as pd

dias_da_semana = { 'Sunday'    : 'Domingo', 
                    'Monday'    : 'Segunda', 
                    'Tuesday'   :'Terça', 
                    'Wednesday' : 'Quarta', 
                    'Thursday'  : 'Quinta', 
                    'Friday'    : 'Sexta', 
                    'Saturday'  :'Sabádo'}

def obter_dias_mes(ano, mes):
    nro_tentativas = 0
    indice = None
    ultimo_dia = 31

    while (nro_tentativas < 5):
        try:
            indice = pd.date_range(start=f'{ano}-{mes}-1', end=f'{ano}-{mes}-{ultimo_dia}')
            
            break
        except ValueError as error:
            assert str(error) == "could not convert string to Timestamp"
        finally:
            ultimo_dia -= 1
            nro_tentativas += 1
    
    return indice
        
