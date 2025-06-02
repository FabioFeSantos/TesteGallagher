# Teste Técnico Gallagher - Fábio Ferreira dos Santos

## Estruturação de Dados

Este repositório contém a solução para a **Estruturação dos Dados**, proposta no processo seletivo para a vaga de **Analista de Dados**.

## Objetivo

Carregar as tabelas Orders, Customers e Web_events fornecida, realizar a ingestão, limpeza e tratamento/transformação dos dados, e estruturá-los em um banco de dados relacional (3º forma normal), tornando-os acessíveis para análises e consultas.


## Tecnologias Utilizadas

- Python 3.12: linguagem principal para manipulação de dados.
- Pandas: biblioteca para leitura, limpeza e integração dos dados.
- JSON: formato de entrada para dados estruturados de clientes.
- Unidecode: biblioteca usada para remover acentuação dos nomes de estados.
- Datetime: manipulação de datas com múltiplos formatos.
- CSV: formato de saída das tabelas tratadas.



## Estrutura do Projeto

```
├── doc/
│   └── Diagrama.drawio      # Diagrama de relacionamento
│   └── diagrama-entidades.png # Imagem do diagrama de relacionamento
│   └── Relatório Final.docx # Arquivo contendo sintese da entrega e considerações
├── src/
│   └── CODIGO_ETL.py      # Script principal de ETL
├── sql/
│   ├── create_table.sql          # Script de criação da tabela no SQL Server
└── README.md                     # Este documento
```

---


# Documentação do Diagrama de Entidades

![Diagrama de Entidades](docs/diagrama-entidades.png)

---

## Tabela: customers

- **Descrição:** Armazena os dados dos clientes do sistema.

| Campo             | Tipo         | Chave         | Descrição                        |
|-------------------|--------------|---------------|----------------------------------|
| customer_id       | INT          | PK            | Identificador único do cliente   |
| full_name         | VARCHAR      |               | Nome completo do cliente         |
| email             | VARCHAR      | UNIQUE        | E-mail do cliente                |
| registration_date | DATE         |               | Data de cadastro do cliente      |
| birth_date        | DATE         |               | Data de nascimento do cliente    |
| phone_number      | VARCHAR      |               | Telefone do cliente              |
| customer_segment  | VARCHAR      |               | Segmento do cliente              |
| state_id          | INT          | FK (states)   | Estado do cliente                |

---

## Tabela: orders

- **Descrição:** Registra os pedidos realizados pelos clientes.

| Campo          | Tipo     | Chave         | Descrição                          |
|----------------|----------|---------------|------------------------------------|
| order_id       | INT      | PK            | Identificador do pedido            |
| customer_id    | INT      | FK (customers)| Cliente que fez o pedido           |
| product_code   | VARCHAR  |               | Código do produto                  |
| order_date     | DATE     |               | Data do pedido                     |
| amount         | DECIMAL  |               | Valor do pedido                    |
| currency       | VARCHAR  |               | Moeda do valor do pedido           |
| order_status   | VARCHAR  |               | Status do pedido                   |
| payment_method | VARCHAR  |               | Método de pagamento do produto     |

---

## Tabela: web_events

- **Descrição:** Armazena eventos de navegação dos clientes.

| Campo          | Tipo     | Chave         | Descrição                          |
|----------------|----------|---------------|------------------------------------|
| event_id       | INT      | PK            | Identificador do evento            |
| customer_id    | INT      | FK (customers)| Cliente relacionado ao evento      |
| event_type     | VARCHAR  |               | Tipo do evento                     |
| event_timestamp| DATETIME |               | Data/hora do evento                |
| page_url       | VARCHAR  |               | Dispositivo utilizado              |
| page           | VARCHAR  |               | Navegador utilizado                |
| referrer       | VARCHAR  |               | Origem do evento                   |

---

## Tabela: states

- **Descrição:** Lista os estados/regiões dos clientes.

| Campo      | Tipo     | Chave | Descrição                |
|------------|----------|-------|--------------------------|
| state_id   | INT      | PK    | Identificador do estado  |
| state_name | VARCHAR  |       | Nome do estado           |
| state_code | VARCHAR  |       | Código do estado         |

---

## Relacionamentos

- `customers.state_id` → `states.state_id`: Cada cliente pertence a um estado.
- `orders.customer_id` → `customers.customer_id`: Cada pedido é feito por um cliente.
- `web_events.customer_id` → `customers.customer_id`: Cada evento de navegação está associado a um cliente.

---

