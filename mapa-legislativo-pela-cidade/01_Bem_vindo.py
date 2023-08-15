import streamlit as st
import random

icons = [
        ':open_file_folder:', ':telescope:',
        ':pushpin:', ':black_nib:',
        ':books:', ':card_index:',
        ':pencil2:', ':pencil:',
        ':bookmark_tabs:', ':calendar:',
        ':memo:', ':chart_with_downwards_trend:',
        ':dart:', ':chart_with_upwards_trend:',
        ':page_with_curl:', ':earth_americas:',
        ':crystal_ball:'
    ]

if __name__ == "__main__":
    icon = random.choice(icons)
    st.title(f"{icon} Matérias legislativas")
