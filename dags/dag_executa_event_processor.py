# dag_executa_script.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import pandas as pd
from sqlalchemy import create_engine

def extracao_armazenamento():
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

    # Inicializando a variável data
    data = {}

    try:
        # Fazendo uma requisição GET
        response = requests.get(url, headers=headers, params=params)

        # Verificando se a requisição foi bem-sucedida (código 200)
        if response.status_code == 200:
            data = response.json()  # Converte a resposta para JSON
            print("Dados recebidos:", data)
        else:
            print(f"Erro na requisição: {response.status_code}, {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer requisição: {e}")

    # Se os dados foram recebidos com sucesso, faz o processamento
    if data:
        try:
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
                print(f'Erro ao inserir os dados no PostgreSQL: {e}')

        except Exception as e:
            print(f"Erro ao processar os dados: {e}")

# Configuração do DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 1, 23),  # Modifique para uma data mais próxima ou passada
    'retries': 2,
    'retry_delay': timedelta(minutes=5),  # Aumentei o intervalo para 5 minutos
}

# Definição do DAG
with DAG(
    dag_id='executa_event_processor',
    default_args=default_args,
    description='DAG para executar outro arquivo Python',
    schedule_interval=timedelta(minutes=5),  # Aumentei o intervalo para 5 minutos
    catchup=False,
) as dag:

    # Definindo a tarefa que executa a função importada
    tarefa = PythonOperator(
        task_id='executar_funcao_do_script',
        python_callable=extracao_armazenamento,  # Função a ser executada
    )

    # Definindo a ordem de execução (se houver mais tarefas no futuro)
    tarefa
