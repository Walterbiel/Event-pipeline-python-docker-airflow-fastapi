from fastapi import FastAPI
import json
import random
from faker import Faker
from datetime import datetime, timedelta

app = FastAPI()
fake = Faker()

# Função para gerar uma data aleatória entre janeiro e dezembro de 2024
def random_date():
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")

# Função para gerar dados de vendas aleatórios
def generate_sales_data(num_records=10):
    sales_data = []
    for _ in range(num_records):
        sale = {
            "cliente": fake.name(),
            "data": random_date(),
            "valor_venda": round(random.uniform(100, 5000), 2)  # Valor entre 100 e 5000
        }
        sales_data.append(sale)
    return sales_data

# Rota para gerar dados de vendas
@app.get("/vendas/")
def get_sales_data(records: int = 10):
    """
    Gera dados aleatórios de vendas.
    Parâmetro:
    - records (int): Número de registros de vendas a serem gerados. Padrão = 10.
    """
    vendas = generate_sales_data(records)
    return {"vendas": vendas}

# Rota raiz de boas-vindas
@app.get("/")
def read_root():
    return {"mensagem": "Bem-vindo à API de geração de dados de vendas!"}
