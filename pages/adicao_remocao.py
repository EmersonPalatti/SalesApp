import streamlit as st
import pandas as pd
from datetime import datetime

from pathlib import Path

from utils import leitura_de_dados


def listar_vendedores(df_filiais: pd.DataFrame, filial_selecionada: str) -> list[str]:
    """Retorna lista de vendedores para a filial selecionada."""
    vendedores_raw = df_filiais.loc[df_filiais['cidade/estado'] == filial_selecionada, 'vendedores'].iloc[0]
    return vendedores_raw.strip('][]').replace("'", "").split(", ")


def adicionar_registro_venda(df_vendas: pd.DataFrame, valores: list) -> pd.DataFrame:
    """Adiciona nova venda, ordena e persiste em CSV."""
    hora_adicionar = datetime.now()
    df_vendas.loc[hora_adicionar] = valores
    df_vendas = df_vendas.sort_values('id_venda', ascending=False)
    df_vendas.to_csv(st.session_state['caminho_datasets'] / 'vendas.csv', decimal=',', sep=';')
    st.session_state['dados']['vendas'] = df_vendas
    st.session_state['dados']['df_vendas'] = df_vendas  # retrocompatibilidade
    return df_vendas


def remover_registro_venda(df_vendas: pd.DataFrame, id_remocao: int) -> pd.DataFrame:
    """Remove venda pelo id, ordena e persiste em CSV."""
    df_vendas = df_vendas[df_vendas['id_venda'] != id_remocao]
    df_vendas = df_vendas.sort_values('id_venda', ascending=False)
    df_vendas.to_csv(st.session_state['caminho_datasets'] / 'vendas.csv', decimal=',', sep=';')
    st.session_state['dados']['vendas'] = df_vendas
    st.session_state['dados']['df_vendas'] = df_vendas
    return df_vendas


def main():
    """Interface para adicionar e remover vendas."""

    st.markdown("## Adição e Remoção de Vendas")
    
    leitura_de_dados()

    dados = st.session_state['dados']
    df_vendas = dados['vendas']
    df_filiais = dados['filiais']
    df_produtos = dados['produtos']

    df_filiais['cidade/estado'] = df_filiais['cidade'] + '/' + df_filiais['estado']
    cidades_filiais = df_filiais['cidade/estado'].to_list()

    st.sidebar.markdown("## Adição de Vendas")
    filial_selecionada = st.sidebar.selectbox("Selecione a filial", cidades_filiais)

    vendedores = listar_vendedores(df_filiais, filial_selecionada)
    vendedor_selecionado = st.sidebar.selectbox("Selecione o vendedor", vendedores)

    produtos = df_produtos['nome'].to_list()
    produto_selecionado = st.sidebar.selectbox("Selecione o produto", produtos)

    nome_cliente = st.sidebar.text_input("Nome do cliente")
    genero_selecionado = st.sidebar.selectbox("Selecione o gênero", ["masculino", "feminino"])

    forma_pagamento = st.sidebar.selectbox("Selecione a forma de pagamento", ["boleto", "pix", "crédito"])

    adicionar_venda = st.sidebar.button("Adicionar Venda")
    if adicionar_venda:
        nova_venda = [
            df_vendas['id_venda'].max() + 1,
            filial_selecionada.split('/')[0],
            vendedor_selecionado,
            produto_selecionado,
            nome_cliente,
            genero_selecionado,
            forma_pagamento,
        ]
        df_vendas = adicionar_registro_venda(df_vendas, nova_venda)

    st.sidebar.markdown("## Remoção de Vendas")
    id_remocao = st.sidebar.number_input("ID da Venda a Remover", min_value=1, max_value=df_vendas['id_venda'].max())
    remover_venda = st.sidebar.button("Remover Venda")
    if remover_venda:
        df_vendas = remover_registro_venda(df_vendas, id_remocao)

    df_vendas = df_vendas.sort_values('id_venda', ascending=False)
    st.dataframe(df_vendas, width='stretch')


if __name__ == "__main__":
    main()

