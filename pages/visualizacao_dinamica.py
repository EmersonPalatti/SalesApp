import streamlit as st
import pandas as pd

from pathlib import Path

from utils import leitura_de_dados, preparar_vendas, formatar_moeda

COLUNAS_ANALISE = ['filial', 'produto', 'vendedor', 'cliente', 'cliente_genero', 'forma_pagamento']
COLUNAS_VALOR = ['preco', 'comissao']
FUNCOES_AGG = {'Soma': 'sum', 'Contagem': 'count'}


def montar_controles(df_vendas: pd.DataFrame):
    """Coleta seleções de índices, colunas, valor e métrica."""
    indice_selecionado = st.sidebar.multiselect('Selecione os índices', COLUNAS_ANALISE)
    col_analises_exc = [c for c in COLUNAS_ANALISE if c not in indice_selecionado]
    colunas_selecionadas = st.sidebar.multiselect('Selecione as colunas', col_analises_exc)

    valor_selecionado = st.sidebar.selectbox('Selecione o valor da análise', COLUNAS_VALOR)
    metrica_selecionada = st.sidebar.selectbox('Selecione a métrica', list(FUNCOES_AGG.keys()))
    return indice_selecionado, colunas_selecionadas, valor_selecionado, FUNCOES_AGG[metrica_selecionada]


def gerar_pivot(df_vendas: pd.DataFrame, indices: list, colunas: list, valor: str, metrica: str):
    """Gera pivot table com totais gerais."""
    tabela = df_vendas.pivot_table(index=indices, columns=colunas, values=valor, aggfunc=metrica)
    tabela['Total Geral'] = tabela.sum(axis=1)
    tabela.loc['Total Geral'] = tabela.sum(axis=0).to_list()
    return tabela


def main():
    """Visualização dinâmica com tabela dinâmica pivot."""
    st.markdown("## Visualização Dinâmica")
    leitura_de_dados()

    dados = st.session_state['dados']
    df_vendas = preparar_vendas(dados['vendas'], dados['produtos'])

    indice_selecionado, colunas_selecionadas, valor_selecionado, metrica_selecionada = montar_controles(df_vendas)

    if len(indice_selecionado) > 0 and len(colunas_selecionadas) > 0:
        vendas_pivotada = gerar_pivot(df_vendas, indice_selecionado, colunas_selecionadas, valor_selecionado, metrica_selecionada)
        st.dataframe(vendas_pivotada)
    else:
        st.info("Selecione ao menos um índice e uma coluna para gerar a tabela.")


if __name__ == "__main__":
    main()




