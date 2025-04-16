import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

# Definir o caminho para o arquivo JSONL
df = pd.read_json('data/data.jsonl', lines=True)

# Setar o pandas para mostrar todas as colunas
pd.options.display.max_columns = None

# Adicionar a coluna _source com um valor fixo
df['_source'] = "https://lista.mercadolivre.com.br/notebook"

# Adicionar a coluna _data_coleta com a data e hora atuais
df['_datetime'] = datetime.now()

# Tratar nulos
df['old_money'] = df['old_money'].fillna('0')
df['new_money'] = df['new_money'].fillna('0')
df['reviews_rating_number'] = df['reviews_rating_number'].fillna('0')
df['reviews_amount'] = df['reviews_amount'].fillna('(0)')

# Garantir que estão como strings antes de usar .str
df['old_money'] = df['old_money'].astype(str).str.replace('.', '', regex=False)
df['new_money'] = df['new_money'].astype(str).str.replace('.', '', regex=False)
df['reviews_amount'] = df['reviews_amount'].astype(str).str.replace('[\(\)]', '', regex=True)

# Converter para números
df['old_money'] = df['old_money'].astype(float)
df['new_money'] = df['new_money'].astype(float)
df['reviews_rating_number'] = df['reviews_rating_number'].astype(float)
df['reviews_amount'] = df['reviews_amount'].astype(int)

# Filtrar produtos com preço entre 1000 e 10000 reais
df = df[
    (df['old_money'] >= 1000) & (df['old_money'] <= 10000) &
    (df['new_money'] >= 1000) & (df['new_money'] <= 10000)
]

# Configurar a conexão com o SQL Server usando SQLAlchemy
server = 'DESKTOP-MGR8475\\SQLEXPRESS'  # Substitua pelo nome do servidor
database = 'Webscraping'  # Substitua pelo nome do banco de dados
username = 'sa'  # Substitua pelo nome do usuário
password = '101083'  # Substitua pela senha do usuário

# Criar a string de conexão para SQLAlchemy
connection_string = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"

# Criar o engine do SQLAlchemy
engine = create_engine(connection_string)

# Salvar o DataFrame no SQL Server em lotes
df.to_sql('notebook', engine, if_exists='replace', index=False, chunksize=1000)

print("Dados salvos no SQL Server com sucesso!")