import streamlit as st

if 'k_links' not in st.session_state:
    st.session_state['k_links'] = 1

def go_up():
    st.session_state['k_links'] = st.session_state.get('k_links', 1) + 1

def go_down():
    k =  st.session_state.get('k_links', 1) - 1
    if k < 1:
        st.session_state['k_links'] = 1
    else :
        st.session_state['k_links'] = k

def main():
    st.title('Pesquisa de Preço')
    for i in range(st.session_state.get('k_links', 1)):
        st.text_input("Link", key=f"link_{i}")
    col_a, col_b = st.columns(2)
    with col_a:
        st.button('Mais', type='primary', on_click=go_up)
    with col_b:
        st.button('Menos', type='primary', on_click=go_down)

    if st.button("Pesquisar") :
        k = st.session_state['k_links']
        links = [st.session_state[f'link_{i}'] for i in range(k)]
        st.write(links)


if __name__ == "__main__":
    main()