# SalesApp

Dashboard de vendas em Streamlit para explorar, editar e visualizar dados de vendas, filiais e produtos.

## Visão geral
- **Stack:** Python 3.14+, Streamlit, Pandas, Plotly, Humanize.
- **Dados:** armazenados em `datasets/` (CSVs gerados pelo script `datasets/gerador_de_vendas.py`).
- **Páginas:** navegação centralizada em `main.py` usando `st.navigation`.

## Estrutura

```
main.py                 # entrypoint Streamlit
utils.py                # utilitários de dados, constantes e formatações
pages/
  home.py               # intro do app
  visao_geral.py        # dashboard com métricas e gráficos
  visualizacao_dinamica.py # pivot dinâmica
  tabelas.py            # exploração tabular e filtros
  adicao_remocao.py     # CRUD simples de vendas
datasets/
  *.csv, *.xlsx         # arquivos de dados
```

## Preparar ambiente

1. Crie e ative um virtualenv (opcional, mas recomendado).
2. Instale dependências (modo desenvolvimento recomendado):

```bash
pip install -e .
```

Requisitos principais definidos em `pyproject.toml`.

## Executar

```bash
streamlit run main.py
```

A navegação lateral exibirá as páginas disponíveis.

## Páginas

- **Home:** descrição rápida do app e bibliotecas usadas.
- **Dashboard de Análise Geral (`pages/visao_geral.py`):** métricas de valor/quantidade, comparação com período anterior, filial/vendedor destaque, linha temporal e pizza por dimensão selecionada.
- **Visualização Dinâmica (`pages/visualizacao_dinamica.py`):** tabela dinâmica configurável (índices, colunas, valor, métrica soma/contagem).
- **Tabelas (`pages/tabelas.py`):** exploração de vendas/filiais/produtos com seleção de colunas e filtro único.
- **Adicionar ou Remover Venda (`pages/adicao_remocao.py`):** inclusão/remoção de registros com persistência em CSV.

## Utilitários
- `leitura_de_dados()`: carrega datasets e injeta em `st.session_state`.
- `preparar_vendas()`: enriquece vendas com preço e comissão (merge com produtos).
- `formatar_moeda()`: formatação monetária pt_BR.
- Constantes: `COMISSAO`, `SELECAO_KEYS` (mapeia labels para colunas nas análises).

## Dados
- Ajuste os CSVs em `datasets/` conforme necessário.
- Para regenerar, utilize o script `datasets/gerador_de_vendas.py` (caso disponível no repo).

## Convenções
- Cada página possui `main()` e docstring breve.
- Evite duplicar lógica de preparo de dados; reutilize helpers em `utils.py`.

## Próximos passos sugeridos
- Adicionar testes simples para utilitários (p.ex., `preparar_vendas`).
- Validar entradas na página de adição (campos obrigatórios, tipos).
- Melhorar estilos (tema Streamlit) e mensagens de status.
