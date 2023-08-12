import random

import sklearn as sk
import spacy
import spacy_streamlit
import streamlit as st

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

st.cache_data
def load_text_data(dataset_name : str):
    result = sk.datasets.fetch_20newsgroups()
    return result['data']



def main():
    nlp = load_model('en-core-web-sm')
    data = load_text_data()

    st.title("Named Entity Recognition example")

    if st.button("Pick random!") :
        random_index = random.randint(0, len(data)-1)
    
    text = data[random_index]
    doc = nlp(text)

    default_visualizer, custom_visualizer = st.tabs([
        "Default NER visualizer",
        "Custom NER visualizer"
    ])

    with default_visualizer:
        visualize_ner(doc, labels=nlp.get_pipe("ner").labels, show_table=False)

    with custom_visualizer:
        st.write("Not yet implemented!")




if __name__ == "__main__" :
    main()