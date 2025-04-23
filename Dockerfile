# ✅ Base leve com Python 3.11
FROM python:3.11-slim-bullseye

# 📍 Definir o diretório de trabalho
WORKDIR /app

# 📦 Instalar dependências do sistema e o driver ODBC do SQL Server
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        gnupg2 \
        unixodbc \
        unixodbc-dev \
        gcc \
        g++ \
        apt-transport-https && \
    curl -sSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg && \
    install -o root -g root -m 644 microsoft.gpg /usr/share/keyrings/ && \
    echo "deb [signed-by=/usr/share/keyrings/microsoft.gpg] https://packages.microsoft.com/debian/11/prod bullseye main" > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
    rm -f microsoft.gpg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 📦 Copiar dependências Python
COPY requirements.txt .

# ✅ Instalar dependências do Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# ✅ Instalar dependências adicionais (Airflow + Streamlit)
RUN pip install apache-airflow==2.6.3 apache-airflow-providers-microsoft-mssql streamlit

# 📦 Copiar o código da aplicação para o container
COPY . .

# 🌐 Expor a porta do Streamlit
EXPOSE 8501

# 🚀 Definir o comando padrão ao iniciar o container
CMD ["streamlit", "run", "src/dashboard/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
