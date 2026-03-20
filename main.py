import streamlit as st

st.set_page_config(
    page_title="SalesApp",
    layout="wide",
    initial_sidebar_state="expanded",
)

pages = {
    "Home": [
        st.Page("pages/home.py", title="Home"),
    ],
    "Dashboards": [
        st.Page("pages/visao_geral.py", title="Dashboard de Análise Geral"),
    ],
    "Tabelas": [
        st.Page("pages/tabelas.py", title="Tabelas"),
        st.Page('pages/visualizacao_dinamica.py', title='Visualização Dinâmica'),
    ],
    'Edição': [
        st.Page("pages/adicao_remocao.py", title="Adicionar ou Remover Venda"),
    ]
}

pg = st.navigation(pages)
pg.run()
