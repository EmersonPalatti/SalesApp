from pathlib import Path

import humanize
import pandas as pd
import streamlit as st

COMISSAO = 0.08
SELECAO_KEYS = {
    'Filial': 'filial',
    'Produto': 'produto',
    'Vendedor': 'vendedor',
    'Forma de Pagamento': 'forma_pagamento',
    'Gênero Cliente': 'cliente_genero',
}


def leitura_de_dados():
    """Carrega csvs e guarda em session_state."""
    pasta_datasets = Path(__file__).parents[0] / 'datasets'

    df_vendas = pd.read_csv(
        pasta_datasets / 'vendas.csv', decimal=',', sep=';', index_col=0, parse_dates=True
    )
    df_filiais = pd.read_csv(pasta_datasets / 'filiais.csv', decimal=',', sep=';', index_col=0)
    df_produtos = pd.read_csv(pasta_datasets / 'produtos.csv', decimal=',', sep=';', index_col=0)

    st.session_state['caminho_datasets'] = pasta_datasets
    st.session_state['dados'] = {
        'vendas': df_vendas,
        'filiais': df_filiais,
        'produtos': df_produtos,
    }


def preparar_vendas(df_vendas: pd.DataFrame, df_produtos: pd.DataFrame) -> pd.DataFrame:
    """Merge de vendas com produtos, adicionando preco e comissao."""
    df_produtos = df_produtos.rename(columns={'nome': 'produto'})
    df_vendas = df_vendas.reset_index()
    df_vendas = pd.merge(df_vendas, df_produtos[['produto', 'preco']], on='produto', how='left')
    df_vendas = df_vendas.set_index('data')
    df_vendas['comissao'] = df_vendas['preco'] * COMISSAO
    return df_vendas


def formatar_moeda(valor: float) -> str:
    humanize.i18n.activate("pt_BR")
    return f"R$ {humanize.intcomma(round(valor, 2))}"