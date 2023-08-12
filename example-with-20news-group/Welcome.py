import random

import spacy
import spacy_streamlit
import streamlit as st
import re
from spacy import displacy
from sklearn.datasets import fetch_20newsgroups
from spacy_streamlit import load_model
from spacy_streamlit import visualize_ner

# st.cache_resource
# def load_model(model : str = 'en_core_web_sm'):
#     nlp = None
#     try:
#         nlp = spacy.load(model)
#     except IOError:
#         print(f"downloading model {model} ...")
#         spacy.cli.download(model)
#         nlp = spacy.load(model)
    
#     return nlp

def load_text_data():
    # it did not work well
    # result = fetch_20newsgroups()
    text = None
    with open('70.txt', 'r', encoding='utf8') as f:
        text = f.read()

    return text



def main():
    st.title("Named Entity Recognition Example")
    nlp = load_model('en_core_web_sm')
    text = load_text_data()
    
    doc = nlp(text)

    default_visualizer, custom_visualizer, raw_text = st.tabs([
        "Default NER visualizer",
        "Custom NER visualizer",
        'Raw text'
    ])

    with default_visualizer:
        visualize_ner(doc, labels=nlp.get_pipe("ner").labels, show_table=False)

    with custom_visualizer:
        html = displacy.render([doc], style='ent')
        # html = re.sub("\s{2,}", " ", html)
        html = re.sub('\n', ' ', html)
        st.markdown(html, unsafe_allow_html=True)

    with raw_text:
        st.text_area('Text:',text)





if __name__ == "__main__" :
    main()