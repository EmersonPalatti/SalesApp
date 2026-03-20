import streamlit as st
import pandas as pd
from datetime import date, timedelta
import plotly.express as px
import humanize

from pathlib import Path

from utils import leitura_de_dados, preparar_vendas, formatar_moeda, SELECAO_KEYS

def main():
    """Dashboard de análises com métricas e gráficos."""
    leitura_de_dados()

    dados = st.session_state['dados']
    df_vendas = dados['vendas']
    df_filiais = dados['filiais']
    df_produtos = dados['produtos']

    df_vendas = preparar_vendas(df_vendas, df_produtos)

    data_final_def = df_vendas.index.date.max()
    data_inicial_def = date(year=data_final_def.year, month=data_final_def.month, day=1)

    data_inicial = st.sidebar.date_input('Data inicial', value=data_inicial_def)
    data_final = st.sidebar.date_input('Data final', value=data_final_def)

    analise_selecionada = st.sidebar.selectbox('Análise', list(SELECAO_KEYS.keys()))
    analise_selecionada = SELECAO_KEYS[analise_selecionada]

    df_vendas_corte = df_vendas[(df_vendas.index.date >= data_inicial) & (df_vendas.index.date <= data_final)].copy()
    df_vendas_corte_anterior = df_vendas[(df_vendas.index.date >= data_inicial - timedelta(days=30)) 
                                        & (df_vendas.index.date <= data_final - timedelta(days=30))].copy()

    st.markdown('# Dashboard de Análises')

    col1, col2, col3, col4 = st.columns(4)

    valor_total = df_vendas_corte["preco"].sum()
    valor_total_anterior = df_vendas_corte_anterior["preco"].sum()
    delta_valor = valor_total - valor_total_anterior

    col1.metric(
        "Valor de vendas do período",
        value=formatar_moeda(valor_total),
        delta=formatar_moeda(delta_valor),
    )

    qtd_total = df_vendas_corte['preco'].count()
    qtd_total_anterior = df_vendas_corte_anterior['preco'].count()
    delta_qtd = qtd_total - qtd_total_anterior

    col2.metric(
        "Qnt de vendas no período",
        value=humanize.intcomma(qtd_total),
        delta=humanize.intcomma(delta_qtd),
    )

    principal_filial = df_vendas_corte.groupby('filial')['preco'].sum().idxmax()
    col3.metric(
        "Filial principal",
        value=principal_filial,
    )

    principal_vendedor = df_vendas_corte.groupby('vendedor')['preco'].sum().idxmax()
    col4.metric(
        "Vendedor principal",
        value=principal_vendedor,
    )

    st.divider()

    col21, col22 = st.columns(2)

    df_vendas_corte['dia_venda'] = df_vendas_corte.index.date
    venda_dia = df_vendas_corte.groupby('dia_venda')['preco'].sum()
    venda_dia.name = 'Venda Valor'

    fig = px.line(venda_dia)
    col21.plotly_chart(fig)

    fig = px.pie(df_vendas_corte, names=analise_selecionada, values='preco')
    col22.plotly_chart(fig)

    st.divider()

if __name__ == "__main__":
    main()