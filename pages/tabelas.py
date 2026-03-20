import streamlit as st
import pandas as pd

from pathlib import Path

from utils import leitura_de_dados


def show_tabela_produtos(df_produtos: pd.DataFrame):
    """Exibe tabela de produtos."""
    st.dataframe(df_produtos, width='stretch')


def show_tabela_filiais(df_filiais: pd.DataFrame):
    """Exibe tabela de filiais."""
    st.dataframe(df_filiais, width='stretch')


def show_tabela_vendas(df_vendas: pd.DataFrame):
    """Exibe vendas com seleção de colunas e filtro único."""
    colunas_selecionadas = st.sidebar.multiselect(
        'Selecione as colunas', list(df_vendas.columns), default=list(df_vendas.columns)
    )

    filtro_box = st.sidebar.container(border=True)
    filtro_selecionado = filtro_box.selectbox('Selecione um filtro:', list(df_vendas.columns))
    valor_unico_col = filtro_box.selectbox('Selecione um valor:', list(df_vendas[filtro_selecionado].unique()))

    col1, col2 = filtro_box.columns(2)
    filtrar = col1.button("Filtrar", width='stretch', type='primary')
    limpar = col2.button("Limpar", width='stretch')

    if filtrar:
        st.dataframe(df_vendas.loc[df_vendas[filtro_selecionado] == valor_unico_col, colunas_selecionadas], width='stretch')
    elif limpar:
        st.dataframe(df_vendas[colunas_selecionadas], width='stretch')
    else:
        st.dataframe(df_vendas[colunas_selecionadas], width='stretch')


def main():
    """Entrada da página de tabelas com seleção de fonte de dados."""

    st.markdown("## Tabelas")
    
    leitura_de_dados()

    dados = st.session_state['dados']
    df_vendas = dados['vendas']
    df_filiais = dados['filiais']
    df_produtos = dados['produtos']

    st.sidebar.title("Filtros")
    tabela_selecionada = st.sidebar.selectbox(
        'Seleciona uma tabela:', ['Vendas', 'Filiais', 'Produtos']
    )

    if tabela_selecionada == 'Produtos':
        show_tabela_produtos(df_produtos)
    elif tabela_selecionada == 'Filiais':
        show_tabela_filiais(df_filiais)
    elif tabela_selecionada == 'Vendas':
        show_tabela_vendas(df_vendas)


if __name__ == "__main__":
    main()

