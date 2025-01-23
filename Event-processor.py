

import requests
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# URL da API
url = "http://127.0.0.1:3000/vendas/?records=50"

# Cabeçalhos (se necessário)
headers = {
    "Content-Type": "application/json"
}

# Parâmetros de consulta (se necessário)
params = {
    "userId": 1
}

# Fazendo uma requisição GET
response = requests.get(url, headers=headers, params=params)

# Verificando se a requisição foi bem-sucedida (código 200)
if response.status_code == 200:
    data = response.json()  # Converte a resposta para JSON
    print("Dados recebidos:", data)
else:
    print(f"Erro na requisição: {response.status_code}, {response.text}")

    #------------------------------------------------------------------------------

# Criando DataFrame
df = pd.DataFrame(data['vendas'])

# Convertendo coluna de data para datetime
df['data'] = pd.to_datetime(df['data'])

# Ordenando os dados por data
df = df.sort_values(by='data')

# Configuração da conexão com o PostgreSQL
db_usuario = 'airflow'
db_senha = 'airflow'
db_host = 'localhost'
db_porta = '5432'
db_nome = 'airflow'

# Criando a string de conexão
engine = create_engine(f'postgresql://{db_usuario}:{db_senha}@{db_host}:{db_porta}/{db_nome}')

# Inserindo os dados no PostgreSQL
tabela_destino = 'airflow'

try:
    df.to_sql(tabela_destino, con=engine, if_exists='append', index=False)
    print(f'Dados inseridos com sucesso na tabela "{tabela_destino}".')
except Exception as e:
    print(f'Erro ao inserir os dados: {e}')

