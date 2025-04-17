







# Importar bibliotecas
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Configurar a conexão com o SQL Server
server = 'DESKTOP-MGR8475\\SQLEXPRESS'  # Substitua pelo nome do servidor
database = 'Webscraping'  # Substitua pelo nome do banco de dados
username = 'sa'  # Substitua pelo nome do usuário
password = '101083'  # Substitua pela senha do usuário

# Criar a string de conexão para SQLAlchemy
connection_string = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"

# Criar o engine do SQLAlchemy
engine = create_engine(connection_string)

# Carregar os dados da tabela 'notebook' em um DataFrame pandas
df = pd.read_sql("SELECT * FROM notebook", engine)

# Título da aplicação
st.title('📊 Pesquisa de Mercado - Notebooks no Mercado Livre')

# Melhorar o layout com colunas para KPIs
st.subheader('💡 KPIs principais')
col1, col2, col3 = st.columns(3)

# KPI 1: Número total de itens
total_itens = df.shape[0]
col1.metric(label="🖥️ Total de Notebooks", value=total_itens)

# KPI 2: Número de marcas únicas
unique_brands = df['brand'].nunique()
col2.metric(label="🏷️ Marcas Únicas", value=unique_brands)

# KPI 3: Preço médio novo (em reais)
average_new_price = df['new_money'].mean()
col3.metric(label="💰 Preço Médio (R$)", value=f"{average_new_price:.2f}")

# Dois gráficos lado a lado (Marcas mais encontradas e Preço médio por marca)
st.subheader('🏆 Marcas mais encontradas até a 10ª página e 💵 Preço médio por marca')
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Marcas mais encontradas")
    top_brands = df['brand'].value_counts().sort_values(ascending=False)
    st.bar_chart(top_brands)

with col2:
    st.markdown("#### Preço médio por marca")
    df_non_zero_prices = df[df['new_money'] > 0]
    average_price_by_brand = df_non_zero_prices.groupby('brand')['new_money'].mean().sort_values(ascending=False)
    st.bar_chart(average_price_by_brand)



# Gráfico de satisfação + Insights estratégicos lado a lado
st.subheader('⭐ Satisfação média por marca')
col1, col2 = st.columns([3, 4])  # Gráfico mais largo, texto mais espaçado

with col1:
    satisfaction_by_brand = (
        df[df['reviews_rating_number'] > 0]
        .groupby('brand')['reviews_rating_number']
        .mean()
        .sort_values(ascending=False)
    )
    st.bar_chart(satisfaction_by_brand)
    st.write("")  # Espaço extra

with col2:
    st.markdown("### Insights Estratégicos sobre a Samsung")
    samsung_rating = satisfaction_by_brand.get('Samsung', None)
    media_geral = satisfaction_by_brand.mean()
    melhor_marca = satisfaction_by_brand.idxmax()
    melhor_nota = satisfaction_by_brand.max()
    posicao = satisfaction_by_brand.rank(ascending=False, method='min').get('Samsung', None)
    total_marcas = satisfaction_by_brand.shape[0]

    if samsung_rating is not None:
        st.write(f"**Nota média Samsung:** {samsung_rating:.2f}")
        st.write(f"**Posição Samsung:** {int(posicao)}º de {total_marcas}")

        st.markdown(f"""
- A Samsung apresenta uma satisfação média de consumidores **{samsung_rating:.2f}**, {"acima" if samsung_rating > media_geral else "abaixo ou igual"} à média geral (**{media_geral:.2f}**).
- A marca com maior satisfação é **{melhor_marca}** (**{melhor_nota:.2f}**).
- Em comparação com as principais concorrentes, a Samsung está na posição **{int(posicao)}** entre {total_marcas} marcas analisadas.
- O posicionamento da Samsung é {"forte" if samsung_rating >= media_geral else "mediano"}: ela {"lidera" if samsung_rating == melhor_nota else "pode avançar"} em avaliações positivas, mas pode melhorar em aspectos como preço ou suporte.
- Recomenda-se monitorar as avaliações negativas para identificar oportunidades de diferenciação e reforçar pontos fortes percebidos pelos consumidores.
""")
    else:
        
        st.markdown("""
**Sugestões e Ações Rápidas:**
- **Presença:** Avalie se a Samsung está entre as marcas mais encontradas e, se não, reforce a exposição dos produtos.
- **Preço:** Compare o preço médio dos notebooks Samsung com os concorrentes para identificar oportunidades de ajuste de posicionamento.
- **Satisfação:** Incentive clientes a deixarem avaliações para construir reputação e permitir análises futuras.
- **Concorrência:** Observe as marcas líderes em satisfação e frequência para inspirar melhorias em produto, preço e atendimento.
""")