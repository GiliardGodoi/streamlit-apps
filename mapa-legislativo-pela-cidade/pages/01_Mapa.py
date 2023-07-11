import streamlit as st
import pandas as pd
import folium

from pathlib import Path
from streamlit_folium import st_folium

st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv(Path('data', 'requerimento-ruas-coordenadas.csv'))
    return df


def main():
    df_reqs = load_data()

    st.header("Mapa das proposições")
    years = df_reqs['ano'].unique()

    with st.sidebar:
        selected_years = st.multiselect("Ano", 
                            options= years,
                            default=years
                            )
    if selected_years:
        df = df_reqs[df_reqs['ano'].isin(selected_years)]
    else:
        st.warning("Você deve selecionar pelo menos um ano!")
        df = df_reqs
    
    CENTER_START = [-23.29, -50.07]
    map = folium.Map(location=CENTER_START, zoom_start=14)
    
    fg = folium.FeatureGroup(name="Markers")
    for _, doc in df.iterrows():
        html = f'<a href="{doc.texto_original}" target="_blank">Req. {doc.numero}/{doc.ano}</a>'
        fg.add_child(
            folium.Marker(
                    [doc.lat, doc.lng], 
                    popup=folium.Popup(html=html, parse_html=False, max_width=100), 
                    lazy=True
            )
        )
    # for _, doc in df.iterrows():
    #     html = f'<a href="{doc.texto_original}" target="_blank">Req. {doc.numero}/{doc.ano}</a>'
    #     fg.add_child(
    #         folium.CircleMarker(
    #                 location=[doc.lat, doc.lng], 
    #                 radius=7,
    #                 fill=True,
    #                 popup=folium.Popup(html=html, parse_html=False, max_width=100), 
    #                 lazy=False
    #         )
    #     )

    output = st_folium(
            map,
            center=CENTER_START,
            feature_group_to_add=fg,
            key='mapa-requerimentos',
            width=1200,
            height=600
        )
    
    # st.write(output)

    st.dataframe(df)

if __name__ == "__main__":
    main()

