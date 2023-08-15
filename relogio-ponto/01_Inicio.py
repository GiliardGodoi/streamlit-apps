import re
from datetime import timedelta
from io import BytesIO, StringIO

import numpy as np
import pandas as pd
import streamlit as st

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
    integer_numeric_attribs = [
        'sequential_number',
        'cod_op',
        'day',
        'month',
        'year',
        'hour',
        'minutes'
    ]
    datetime_attrs = [ 'year', 'month', 'day', 'hour', 'minutes']

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
    frame[integer_numeric_attribs] = frame[integer_numeric_attribs].astype(int)
    frame['datetime']  = pd.to_datetime(frame[datetime_attrs])
    frame = frame.drop(columns=datetime_attrs)
    frame = frame.set_index("sequential_number")

    # frame = frame.set_index(['datetime'])

    return frame

def to_excel(df):
    '''
    See the discussion on <https://stackoverflow.com/questions/67564627/how-to-download-excel-file-in-python-and-streamlit>
    '''
    output = BytesIO()
    # writer = pd.ExcelWriter(output, engine='openpyxl') # xlsxwriter
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=True, sheet_name='Plan1')
    # workbook = writer.book
    # worksheet = writer.sheets['Sheet1']
    # format1 = workbook.add_format({'num_format': '0.00'})
    # worksheet.set_column('A:A', None, format1)
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def main():
    st.header(":alarm_clock: Relógio ponto")

    file = st.file_uploader("Subir arquivo")

    if st.button("Upload") and (file is not None):
        df = analisar_arquivo(file)
        st.session_state['dataframe'] = df
    elif (file is None):
        st.session_state['dataframe'] = None

    if type(st.session_state['dataframe']) is pd.DataFrame:
        st.divider()
        df = st.session_state['dataframe']
        '''### Filtrar registros'''
        col1, col2 = st.columns([1, 1])
        with col1:
            mininum_date = df['datetime'].min()
            maximum_date = df['datetime'].max()
            start_date = df['datetime'].max() - timedelta(days=30)
            start_date = start_date if start_date > mininum_date else mininum_date

            start_date = st.date_input("Data inicial:",
                                    min_value=mininum_date,
                                    max_value=maximum_date,
                                    value=start_date,
                                    format="DD/MM/YYYY")

        with col2:
            end_date = st.date_input("Data final:",
                                    min_value=mininum_date,
                                    max_value=maximum_date,
                                    value=maximum_date,
                                    format="DD/MM/YYYY")
        if start_date < end_date:
            df = df.loc[lambda d: (d.datetime.dt.date >= start_date) & (d.datetime.dt.date <= end_date) ]
        else:
            st.info("A data inicial deve ser menor que a data final")


        pis_codes = df['pis'].unique()

        selected_pis_code = st.selectbox("Pis code:", options=pis_codes)

        # if st.button("Filtrar",
        #              help="Filtra os registros de acordo com os valores selecionados",
        #              type='secondary'
        #             ):
        df = df.loc[lambda d: d.pis == selected_pis_code]

        '''### Visualizar dados'''
        st.dataframe(df, use_container_width=True)

        if st.button("Computar") :
            st.divider()
            '''### Tabela de horários'''
            df_tmp = df.copy()
            df_tmp['date'] = df.datetime.dt.date
            df_tmp['rank'] = df.groupby([
                df.datetime.dt.month,
                df.datetime.dt.day
            ])['datetime'].rank().astype(int)

            df_ponto = df_tmp.pivot(index='date', columns='rank', values='datetime')
            date_index = pd.date_range(
                start=start_date,
                end=end_date,
                inclusive='both',
                normalize=False,
                freq='D'
            )
            df_ponto = df_ponto.reindex(date_index.date)
            df_ponto.insert(0, 'day name', date_index.day_name())

            st.dataframe(df_ponto, use_container_width=True)

            # st.download_button(":inbox_tray: Download",
            #                 data=to_excel(df_ponto),
            #                 file_name='output.xlsx'
            #                 )
            st.download_button(
                ":inbox_tray: Download",
                df_ponto.to_csv(),
                "output.csv",
                "text/csv",
                key='download-csv'
            )


if __name__ == "__main__":
    main()