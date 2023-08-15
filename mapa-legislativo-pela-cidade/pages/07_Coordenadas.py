import streamlit as st
import pandas as pd
import folium
import requests
from folium.plugins import Draw
from streamlit_folium import st_folium

st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    return None

if 'places' not in st.session_state:
    st.session_state['places'] = list()

def main():

    st.header("Pesquisar coordenadas")

    CENTER_START = [-23.29, -50.07]
    # tiles="cartodb positron"
    # tiles="Stamen Toner"
    map = folium.Map(location=CENTER_START, zoom_start=14)
    draw = Draw(
        export=True,
        draw_options={'polyline' : False, 'polygon': False, 'rectangle' : False,
                      'circle' : False, 'circlemarker' : False, 'marker' : True}
    )
    draw.add_to(map)
    col1, col2 = st.columns([0.7, 0.3], gap='small')

    with col1 :
        output = st_folium(
                map,
                center=CENTER_START,
                key='mapa-coordenadas',
                width=900,
                height=600,
                returned_objects=['last_clicked', 'all_drawings']
            )
    is_available = (output is not None) \
            and ('all_drawings' in output) \
            and (output['all_drawings'] is not None) \
            and (len(output['all_drawings']) > 0)
    with col2:
        if is_available:
            drawings = [d['geometry'] for d in output['all_drawings']]
            st.write("Pontos selecionados")
            df = pd.DataFrame(drawings)
            st.dataframe(df, use_container_width=True, height=500, )

    submit = st.button("Procurar", disabled=(not is_available))
    if submit and is_available:
        st.session_state['places'] = list()
        geometries = [d['geometry'] for d in output['all_drawings']]
        with st.spinner("Pesquisando..."):
            for geometry in geometries:
                lng, lat = geometry['coordinates']
                url = f"https://geocode.maps.co/reverse?lat={lat}&lon={lng}"
                print(url)
                response = requests.get(url)
                st.session_state['places'].append(response.json())

    if st.session_state['places'] :
        st.write(st.session_state['places'])


if __name__ == "__main__":
    main()
