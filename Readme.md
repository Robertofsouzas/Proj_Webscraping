# Projeto Web Scraping Mercado Livre Case Samsung

## Objetivo

O objetivo deste projeto é automatizar a extração de dados do Mercado Livre, processá-los com o Pandas e armazená-los em um banco de dados SQL Server. Além disso, será criada uma dashboard interativa com o Streamlit para visualização e análise dos dados coletados. 

Este projeto foi desenvolvido para ajudar a **Samsung** a comparar seus notebooks com a concorrência.

## Tecnologias Utilizadas

- **Scrapy**: Framework para realizar o web scraping.
- **Pandas**: Biblioteca para manipulação e análise de dados.
- **SQL Server**: Banco de dados para armazenar as informações coletadas.
- **Streamlit**: Ferramenta para criar dashboards interativas.

## Como usar

### 1. Certifique-se de ter o Python instalado.
### 2. Instale as dependências necessárias:
   ```bash
   pip install -r requirements.txt
   ```
### 3. Execute o script principal para iniciar o web scraping:
   ```bash
   scrapy crawl nome_do_spider
   ```
### 4. Após a coleta de dados, execute o script para carregar os dados no SQL Server.
### 5. Por fim, inicie a dashboard com o Streamlit:
   ```bash
   streamlit run dashboard.py
   ```

## Estrutura do Projeto

- `main.py`: Script principal para executar o web scraping.
- `spiders/`: Contém os spiders do Scrapy para realizar a extração de dados.
- `data_processing.py`: Script para processar os dados com o Pandas.
- `database.py`: Script para carregar os dados no SQL Server.
- `dashboard.py`: Script para criar a dashboard no Streamlit.

## Requisitos

- Python 3.x
- SQL Server
- Bibliotecas necessárias (Scrapy, Pandas, Streamlit, etc.).

## Observação

Este projeto é apenas para fins educacionais. Certifique-se de respeitar os Termos de Serviço do site ao realizar web scraping.

## Pipeline do Processo ETL

Abaixo está uma ilustração do pipeline de todo o processo de ETL (Extração, Transformação e Carregamento) deste projeto:

1. **Extração**: Os dados são coletados do site do Mercado Livre utilizando o Scrapy.
2. **Transformação**: Os dados são processados e limpos com o Pandas.
3. **Carregamento**: Os dados transformados são armazenados no banco de dados SQL Server.
4. **Análise**: Os dados são visualizados e analisados em uma dashboard interativa criada com Streamlit.

![Pipeline do Processo ETL](pipeline_etl.png)