### Criação de dados com faker e fastapi, orquestração do pipeline com docker, armazenamento no postgres e visualização em tempo real

#### Digite no terminal: Certifique de ter o docker instalado
 $ docker compose up -d

  #### Após o termino do comando anterior digite: Para colocar em produção o "Event-producer.py"
  uvicorn Event-producer:app --reload --port 3000

### Acesse a API no navegador ou no Postman:

Página inicial: http://127.0.0.1:3000
Gerar 10 vendas: http://127.0.0.1:3000/vendas/
Gerar 50 vendas: http://127.0.0.1:3000/vendas/?records=50





#### Após isso vamos processar essa API com o Event-processor.py que será orquestrado para rodar a cada 5 segundos pelo airflow:

Esse código faz uma requisição na API, transforma o json em um dataframe e adiciona no postgres que pode ser visualizado pelo pgadmin4:




