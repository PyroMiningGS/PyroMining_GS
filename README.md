# Pyro Mining - Prever para Proteger

---

## Visão Geral do Projeto

O **Pyro Mining** é uma solução completa e operacional para previsão de risco de incêndios florestais no Brasil. O projeto integra **engenharia de dados moderna**, **infraestrutura em contêineres**, **aprendizado de máquina com PyTorch**, e **monitoramento via dashboards**, com base em dados meteorológicos públicos do INMET. Ele aplica o Índice de **Monte Alegre Alterada (FMA+)** como referência para geração de rótulos e decisão de alerta. A arquitetura é centrada em dois fluxos de dados principais:

* **Processamento em batch**, que coleta, trata e armazena dados meteorológicos históricos em um data warehouse PostgreSQL e utiliza Power BI e MLflow para visualização e governança.
* **Processamento em tempo real**, que consome eventos via Kafka, realiza predições no MLflow e envia e-mails automáticos quando o risco é considerado **grave** ou **perigosíssimo**.

Essa solução é ideal para aplicações ambientais, defesa civil e prevenção de desastres naturais.

---

## Fundamento Científico: Índice de Nesterov

O índice de Monte Alegre Alterada (FMA+) é indicador de variáveis como temperatura, umidade e vento. Ele foi desenvolvido por pesquisadores brasileiros e é bem adaptado ao clima do país. Baseado em uma combinação de fatores meteorológicos como:

* Temperatura máxima diária
* Umidade relativa mínima
* Número de dias consecutivos sem chuva

O resultado é uma classificação em faixas de risco (baixo, moderado, alto, muito alto, grave, perigosíssimo), que são utilizadas como **labels supervisionados** para treinamento do modelo de machine learning.

---

## Modelo de Machine Learning

* **Framework:** PyTorch
* **Algoritmo:** `MultiHorizonClassifier`
* **Tipo:** Classificador multiclasse com janelas temporais
* **Registro e serving:** MLflow Tracking
* **Treinamento:** Feito sobre os dados tratados da camada Gold

---

## Arquitetura: Pipeline de Batch Processing

```
+--------------------------+
| Dados Meteorológicos CSV |
|        (INMET)           |
+--------------------------+
              |
              v
        [ Armazenado ]
        [   MinIO    ]
              |
              v
+--------------------------+
| Bronze Layer             |
| Dados brutos             |
+--------------------------+
              |
              v
+--------------------------+
| Silver Layer             |
| Limpeza, padronização    |
+--------------------------+
              |
              v
+--------------------------+
| Gold Layer               |
| Feature engineering,     |
| cálculo de índice        |
+--------------------------+
       |             |
       |             v
       |      +------------------+
       |      | PostgreSQL       |
       |      | (Warehouse)      |
       |      +------------------+
       |             |
       |             v
       |      +------------------+
       |      | Power BI         |
       |      | (Dashboard)      |
       |      +------------------+
       |
       v
+--------------------------+
| MLflow                   |
| Avaliação e registro     |
+--------------------------+
```

---

## Arquitetura: Pipeline de Real-Time Processing

```
+----------------------------+
| Kafka (mensagem JSON por h)|
+----------------------------+
              |
              v
+--------------------------+
| Bronze Layer             |
| Dados crus do Kafka      |
+--------------------------+
              |
              v
+--------------------------+
| Silver Layer             |
| Tratamento, parsing      |
+--------------------------+
              |
              v
+--------------------------+
| Gold Layer               |
| Features + índice        |
+--------------------------+
              |
              v
+--------------------------+
| Inferência MLflow        |
| (MultiHorizonClassifier) |
+--------------------------+
              |
         +----+----+
         | Risco?  |
         +----+----+
              |
    +---------+---------+
    |                   |
 [Grave/Perigoso?]    [Outros]
    |                   |
    v                   v
+-----------------+   (Ignora)
| Envia E-mail    |
| com Alerta      |
+-----------------+
              |
              v
+-------------------------------+
| Grava resultado da predição   |
| na tabela `gold_predict`       |
| para Power BI consumir as      |
| previsões de risco para        |
| 1, 6 e 12 horas futuras        |
+-------------------------------+
```

> **Observação:** A tabela `gold_predict` contém previsões futuras e não representa certeza absoluta. Ela é distinta da tabela batch que alimenta o Power BI com dados históricos consolidados.

---

## Dashboards e Interfaces

| Recurso               | Imagem Estática                        |
| --------------------- | -------------------------------------- |
| Power BI Dashboard | <img width="464" height="389" alt="Image" src="https://github.com/user-attachments/assets/9fe1a922-c8e0-47b4-979a-bdd2ee2dec37" /> |
| MLflow Tracking    | <img width="805" height="393" alt="Image" src="https://github.com/user-attachments/assets/d28035d1-a162-431c-bdb5-35fc8b2899e1" /> |
| DAGs Airflow      | <img width="847" height="356" alt="Image" src="https://github.com/user-attachments/assets/7a790b87-c328-49fb-9908-ffed5c7a1e88" /> |
| E-mail de Alerta   | <img width="364" height="440" alt="Image" src="https://github.com/user-attachments/assets/8ac430b5-b53d-4df0-86a4-9dbc7a42c788" /> |

---

## 🧪 Tecnologias Utilizadas

* **Python & PyTorch** – Treinamento e inferência do modelo `MultiHorizonClassifier`
* **Apache Kafka** – Mensageria para ingestão em tempo real
* **Airflow** – Orquestração dos jobs
* **MinIO** – Data lake para ingestão inicial de dados do INMET
* **PostgreSQL** – Armazenamento em warehouse dos dados finais
* **MLflow** – Gestão de modelos, versionamento e serving
* **Power BI** – Dashboard de análise de risco
* **Docker & Compose** – Ambiente conteinerizado
* **SMTP (e-mail)** – Envio de alertas de alto risco

---

## Como Rodar o Projeto

### 1. Clone o repositório

```bash
git clone https://github.com/AzyonDatamining/Azyon.git
cd PyroMining
```

### 2. Configure seu `.env`

```bash
cp .env.example .env
```

Preencha com seus dados.

### 3. Suba os serviços com Docker Compose

```bash
docker-compose up --build
```

---

## 📁 Exemplo de `.env`

```env
POSTGRES_USER=admin 
POSTGRES_PASSWORD=admin123 
POSTGRES_DB=pyromining

EMAIL_USER=example@email.com
EMAIL_PASSWORD=password

MINIO_ACCESS_KEY=minio
MINIO_SECRET_KEY=minio123
MINIO_BUCKET=inmet-data

MLFLOW_TRACKING_URI=http://localhost:5000
MLFLOW_EXPERIMENT_NAME=fire-risk-model

KAFKA_BROKER=localhost:9092
KAFKA_TOPIC=fire-risk-input

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=seu@email.com
EMAIL_PASS=sua_senha

AIRFLOW__CORE__EXECUTOR=LocalExecutor
AIRFLOW__CORE__FERNET_KEY=uma_chave_aqui
```

---

## 🐳 docker-compose.yml completo

```yaml
services:

  postgres:
    image: postgres:14
    restart: always
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

  minio:
    image: minio/minio
    command: server /data --console-address ":9001"
    environment:
      MINIO_ACCESS_KEY: ${MINIO_ACCESS_KEY}
      MINIO_SECRET_KEY: ${MINIO_SECRET_KEY}
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - minio_data:/data

  kafka:
    image: bitnami/kafka:latest
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_CFG_LISTENERS: PLAINTEXT://:9092
      KAFKA_CFG_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      ALLOW_PLAINTEXT_LISTENER: yes

  mlflow:
    image: ghcr.io/mlflow/mlflow:latest
    ports:
      - "5000:5000"
    command: mlflow server --host 0.0.0.0 --port 5000 --backend-store-uri sqlite:///mlflow.db --default-artifact-root /mlruns
    volumes:
      - ./mlruns:/mlruns
      - ./mlflow.db:/mlflow.db

  airflow:
    image: apache/airflow:2.9.1
    environment:
      - AIRFLOW__CORE__EXECUTOR=${AIRFLOW__CORE__EXECUTOR}
      - AIRFLOW__CORE__FERNET_KEY=${AIRFLOW__CORE__FERNET_KEY}
    ports:
      - "8080:8080"
    volumes:
      - ./dags:/opt/airflow/dags
      - airflow_logs:/opt/airflow/logs
    command: bash -c "airflow db init && airflow users create --username admin --firstname admin --lastname admin --role Admin --email admin@example.com --password admin && airflow webserver"

volumes:
  pgdata:
  minio_data:
  airflow_logs:
```
---

> ℹ️ **Este projeto foi selecionado como a melhor ideação, no Desafio PROTECH THE FUTURE! 
> Desenvolvido com base no conteúdo prático do Global Solution aplicado pela FIAP – 1º Semestre de Data Science**,  
> com os integrantes: **Caio Palermo**, **Iago Campos** e **Jonathan Moreira**
