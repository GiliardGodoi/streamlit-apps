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


def main():
    
    st.header("Coordenadas")
        
    CENTER_START = [-23.29, -50.07]
    # tiles="cartodb positron"
    # tiles="Stamen Toner"
    map = folium.Map(location=CENTER_START, zoom_start=14)
    # Draw(export=True).add_to(map)
    col1, col2 = st.columns([0.7, 0.3], gap='small')
    
    with col1 :
        output = st_folium(
                map,
                center=CENTER_START,
                key='mapa-coordenadas',
                width=900,
                height=600,
                returned_objects=['last_clicked']
            )  
    if output is not None \
        and 'last_clicked' in output \
        and output['last_clicked'] is not None :
        lat = output['last_clicked']['lat']
        lng = output['last_clicked']['lng']
    else :
        lat = 0
        lng = 0
    with col2:
        A, B = st.columns(2)
        with A:
            st.text_input("Lat", value=lat)
        with B:
            st.text_input("Long", value=lng)

        submit = st.button('Procurar')
        if submit:
            url = f"https://geocode.maps.co/reverse?lat={lat}&lon={lng}"
            response = requests.get(url)
            st.write(response.json())

if __name__ == "__main__":
    main()

