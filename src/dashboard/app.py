# Importar bibliotecas
import streamlit as st
import pandas as pd
import urllib
from sqlalchemy import create_engine,text
import plotly.express as px

# Configurar a string de conexão
params = urllib.parse.quote_plus(
    "DRIVER=ODBC Driver 17 for SQL Server;"
    "SERVER=192.168.1.105,1433;"
    "DATABASE=Webscraping;"
    "UID=sa;"
    "PWD=101083;"
    "TrustServerCertificate=yes;"
    "Encrypt=no"
)

connection_string = f"mssql+pyodbc:///?odbc_connect={params}"

# Criar engine
engine = create_engine(
    connection_string,
    fast_executemany=True,
    connect_args={
        'autocommit': True,
        'timeout': 30
    }
)

# Testar conexão
try:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))  # ENVOLVER COM text()
        st.success("✅ Conexão com o banco de dados estabelecida com sucesso!")
except Exception as e:
    st.error(f"❌ Erro ao conectar ao banco de dados: {str(e)}")
    st.stop()

# Carregar dados com raw_connection
try:
    # Método 1: Obter uma conexão raw e fechá-la explicitamente
    raw_conn = engine.raw_connection()
    try:
        df = pd.read_sql("SELECT * FROM notebook", raw_conn)
        st.success(f"✅ Dados carregados com sucesso! Total de registros: {len(df)}")
    finally:
        raw_conn.close()
        
    # OU Método 2: Usar engine.connect() com gerenciador de contexto
    # with engine.connect() as connection:
    #     df = pd.read_sql("SELECT * FROM notebook", connection)
    # st.success(f"✅ Dados carregados com sucesso! Total de registros: {len(df)}")
except Exception as e:
    import traceback
    st.error(f"❌ Erro ao carregar os dados: {str(e)}")
    st.error(f"Detalhes: {traceback.format_exc()}")
    st.stop()

# Verificações iniciais
if df.empty:
    st.error("A tabela 'notebook' está vazia.")
    st.stop()

required_columns = ['brand', 'new_money', 'reviews_rating_number']
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    st.error(f"Colunas ausentes: {', '.join(missing_columns)}")
    st.stop()

# Preencher nulos
df['new_money'] = df['new_money'].fillna(0)
df['reviews_rating_number'] = df['reviews_rating_number'].fillna(0)

# Título principal
st.title('📊 Pesquisa de Mercado - Notebooks no Mercado Livre')

# KPIs
st.subheader('💡 KPIs principais')
col1, col2, col3 = st.columns(3)

col1.metric("🖥️ Total de Notebooks", df.shape[0])
col2.metric("🏷️ Marcas Únicas", df['brand'].nunique())
col3.metric("💰 Preço Médio (R$)", f"{df['new_money'].mean():.2f}")

# Abas interativas
st.subheader("📊 Análises Interativas")
tab1, tab2, tab3 = st.tabs(["📈 Marcas & Preços", "⭐ Satisfação", "📥 Exportar dados"])

# Aba 1 - Marcas & Preços
with tab1:
    st.markdown("### 🔝 Top 10 Marcas")
    top_brands_df = df['brand'].value_counts().head(10).reset_index()
    top_brands_df.columns = ['Marca', 'Contagem']
    fig1 = px.bar(top_brands_df, x='Marca', y='Contagem', title='Top Marcas Encontradas')
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("### 💰 Preço médio por marca (Top 10)")
    price_df = (
        df[df['new_money'] > 0]
        .groupby('brand')['new_money']
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    price_df.columns = ['Marca', 'Preço Médio (R$)']
    fig2 = px.bar(price_df, x='Marca', y='Preço Médio (R$)', title='Preço Médio por Marca')
    st.plotly_chart(fig2, use_container_width=True)

# Aba 2 - Satisfação
with tab2:
    st.markdown("### ⭐ Satisfação Média por Marca (Top 10)")
    satisfaction_df = (
        df[df['reviews_rating_number'] > 0]
        .groupby('brand')['reviews_rating_number']
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    satisfaction_df.columns = ['Marca', 'Nota Média']
    fig3 = px.bar(satisfaction_df, x='Marca', y='Nota Média', title='Satisfação Média por Marca')
    st.plotly_chart(fig3, use_container_width=True)

    # Insights sobre Samsung
    st.markdown("### 📌 Insights Personalizados por Marca")

    df['brand'] = df['brand'].fillna('')
    marca_escolhida = st.selectbox("Escolha uma marca para ver os insights:", sorted(df['brand'].unique()))

    if marca_escolhida in df['brand'].values:
        marca_df = df[df['brand'] == marca_escolhida]
        nota_marca = marca_df['reviews_rating_number'].mean()
        nota_marca = 0 if pd.isna(nota_marca) else nota_marca

        media_geral = df[df['reviews_rating_number'] > 0]['reviews_rating_number'].mean()

        brand_avg = (
            df[df['reviews_rating_number'] > 0]
            .groupby('brand')['reviews_rating_number']
            .mean()
            .sort_values(ascending=False)
            .reset_index()
        )

        if not brand_avg[brand_avg['brand'] == marca_escolhida].empty:
            posicao = brand_avg[brand_avg['brand'] == marca_escolhida].index[0] + 1
        else:
            posicao = "fora do Top 10"

        melhor_marca = brand_avg.iloc[0]['brand']
        melhor_nota = brand_avg.iloc[0]['reviews_rating_number']

        col1, col2, col3 = st.columns(3)
        col1.metric("Nota média da marca", f"{nota_marca:.2f}")
        col2.metric("Nota média geral", f"{media_geral:.2f}")
        col3.metric("Posição da marca", f"{posicao}")

        st.markdown(f"""
        - A marca **{marca_escolhida}** tem uma nota de **{nota_marca:.2f}**, {"🟢 acima" if nota_marca > media_geral else "🔴 abaixo"} da média geral (**{media_geral:.2f}**).
        - A marca com melhor satisfação é **{melhor_marca}** com **{melhor_nota:.2f}**.
        - {f"{marca_escolhida} está na **{posicao}ª posição** entre as marcas analisadas." if isinstance(posicao, int) else f"{marca_escolhida} não está entre as 10 mais bem avaliadas."}
        - Explore formas de aumentar a satisfação da marca com melhorias em preço, suporte ou desempenho.
        """)

        # Comparativo visual
        comparativo_df = pd.DataFrame({
            "Categoria": [f"{marca_escolhida}", "Média Geral", f"Top 1: {melhor_marca}"],
            "Nota Média": [nota_marca, media_geral, melhor_nota]
        })
        fig_comp = px.bar(comparativo_df, x="Categoria", y="Nota Média", title="Comparativo de Satisfação")
        st.plotly_chart(fig_comp, use_container_width=True)

    else:
        st.warning(f"{marca_escolhida} não possui avaliações suficientes para gerar insights.")


# Aba 3 - Exportação
with tab3:
    st.markdown("### 📤 Exportar dados filtrados")

    # Preparar lista de marcas (limpando nulos e strings vazias)
    brand_list = sorted([b for b in df['brand'].dropna().unique() if str(b).strip() != ""])
    brand_filter = st.selectbox("Filtrar por marca", options=["Todas"] + brand_list)

    # Aplicar filtro
    df_filtered = df if brand_filter == "Todas" else df[df['brand'] == brand_filter]

    st.dataframe(df_filtered)

    # Exportar CSV
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    nome_arquivo = f"{brand_filter}_notebooks.csv" if brand_filter != "Todas" else "todos_notebooks.csv"
    st.download_button(
        label="📥 Baixar CSV",
        data=csv,
        file_name=nome_arquivo,
        mime='text/csv'
    )

