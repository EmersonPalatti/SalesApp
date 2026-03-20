import streamlit as st


def main():
    """Página inicial com descrição da aplicação."""
    st.title("Bem-vindo ao Analisador de Vendas")
    st.divider()

    st.write(
        """
Utilizaremos três principais bibliotecas:

- `pandas` - para manipulação de dados
- `streamlit` - para criação de aplicativos web
- `plotly` - para visualização de dados

Os dados utilizados foram gerados pelo script `gerador_de_vendas.py` que se encontra junto com o código fonte do projeto. Os dados podem ser visualizados na aba tabelas.
        """
    )


if __name__ == "__main__":
    main()
