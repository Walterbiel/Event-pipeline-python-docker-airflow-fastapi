# dag_executa_script.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# Importando a função do arquivo 'meu_script.py'
from Event_processor import extracao_armazenamento

# Configuração do DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 1, 23),
    'retries': 2,
    'retry_delay': timedelta(seconds=10),
}

with DAG(
    dag_id='executa_outro_arquivo',
    default_args=default_args,
    description='DAG para executar outro arquivo Python',
    schedule_interval='@daily',  # Exemplo de agendamento diário
    catchup=False,
) as dag:

    # Definindo a tarefa que executa a função importada
    tarefa = PythonOperator(
        task_id='executar_funcao_do_script',
        python_callable=extracao_armazenamento,  # Função a ser executada
    )

    tarefa
