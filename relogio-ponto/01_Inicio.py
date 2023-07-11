import numpy as np
import pandas as pd
import re
import streamlit as st

from io import StringIO

# Configuring session state
if 'dataframe' not in st.session_state:
    st.session_state['dataframe'] = None

def analisar_arquivo(uploaded_file):
    pattern = re.compile("(\d{9})(\d{1})(\d{2})(\d{2})(\d{4})(\d{2})(\d{2})(\w{0,1})(\d{12})([\D]+)")
    data = list()
    columns = [
        'sequential_number',
        'cod_op',
        'day',
        'month',
        'year',
        'hour',
        'minutes',
        'cod_input',
        'pis',
        'name'
    ]
    numeric_attribs = [
        'sequential_number', 
        'cod_op', 
        'day', 
        'month', 
        'year', 
        'hour', 
        'minutes' 
    ]
    date_attribs = [ 'year', 'month', 'day', 'hour', 'minutes']
    
    opened_file = StringIO(uploaded_file.getvalue().decode("ISO8859-1"))
    
    for line in opened_file:
        match = pattern.fullmatch(line)
        if match:
            data.append(match.groups())
        else:
            print(line)

    frame = pd.DataFrame(data, columns=columns)
    frame['name'] = frame.name.str.strip('[ \n]')
    frame[['name', 'cod_input']] = frame[['name', 'cod_input']].replace('', np.nan)
    frame[numeric_attribs] = frame[numeric_attribs].astype(int)
    frame['datetime']  = pd.to_datetime(frame[date_attribs])

    return frame


def main():
    st.header(":alarm_clock: Relógio ponto")

    file = st.file_uploader("Subir arquivo")

    if st.button("Upload") :
        df = analisar_arquivo(file)
        st.session_state['dataframe'] = df

    if type(st.session_state['dataframe']) is pd.DataFrame:
        '''## Visualizar dados'''
        st.dataframe(df)

if __name__ == "__main__":
    main()