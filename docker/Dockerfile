FROM python:3.11-slim-bullseye

# Instalar dependências do sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        gnupg2 \
        unixodbc-dev \
        gcc \
        g++ \
        apt-transport-https && \
    # Adicionar repositório Microsoft
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update --fix-missing && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Instalar dependências do Python
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Instalar o Apache Airflow
RUN pip install apache-airflow==2.6.3 apache-airflow-providers-microsoft-mssql

# Copiar o código da aplicação
COPY . .

CMD ["bash"]