import pandas as pd
import json
import unidecode
from datetime import datetime

# 1. Carregar dados
orders = pd.read_csv('orders.csv')
customers = pd.read_json('customers.json')
web_events = pd.read_csv('web_events.csv')

# 2. Limpeza e padronização

# a) Padronizar datas
def parse_date_flex(date_str):
    if pd.isnull(date_str):
        return pd.NaT
    date_str = str(date_str).strip()
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(date_str, fmt)
        except:
            continue
    return pd.NaT

orders['order_date'] = orders['order_date'].astype(str).apply(parse_date_flex)
web_events['event_timestamp'] = web_events['event_timestamp'].astype(str).apply(parse_date_flex)
customers['registration_date'] = customers['registration_date'].astype(str).apply(parse_date_flex)


# b) Retirar duplicidades de clientes por email (case-insensitive), mantendo o registro mais recente
customers['email'] = customers['email'].str.lower()
customers['registration_date'] = pd.to_datetime(customers['registration_date'], dayfirst=True, errors='coerce')
customers = customers.sort_values('registration_date').drop_duplicates('email', keep='last')

# c) Padronizar valores monetários
orders['amount'] = orders['amount'].astype(str).str.replace(',', '.', regex=False).astype(float)

# d) Retirar espaços desnecessários
web_events["user_agent"] = web_events["user_agent"].str.replace(" ", "", regex=False)

# e) Padronizar estados
states = pd.DataFrame([
    {"state_id": 1, "state_name": "Acre", "state_code": "AC"},
    {"state_id": 2, "state_name": "Alagoas", "state_code": "AL"},
    {"state_id": 3, "state_name": "Amapá", "state_code": "AP"},
    {"state_id": 4, "state_name": "Amazonas", "state_code": "AM"},
    {"state_id": 5, "state_name": "Bahia", "state_code": "BA"},
    {"state_id": 6, "state_name": "Ceará", "state_code": "CE"},
    {"state_id": 7, "state_name": "Distrito Federal", "state_code": "DF"},
    {"state_id": 8, "state_name": "Espírito Santo", "state_code": "ES"},
    {"state_id": 9, "state_name": "Goiás", "state_code": "GO"},
    {"state_id": 10, "state_name": "Maranhão", "state_code": "MA"},
    {"state_id": 11, "state_name": "Mato Grosso", "state_code": "MT"},
    {"state_id": 12, "state_name": "Mato Grosso do Sul", "state_code": "MS"},
    {"state_id": 13, "state_name": "Minas Gerais", "state_code": "MG"},
    {"state_id": 14, "state_name": "Pará", "state_code": "PA"},
    {"state_id": 15, "state_name": "Paraíba", "state_code": "PB"},
    {"state_id": 16, "state_name": "Paraná", "state_code": "PR"},
    {"state_id": 17, "state_name": "Pernambuco", "state_code": "PE"},
    {"state_id": 18, "state_name": "Piauí", "state_code": "PI"},
    {"state_id": 19, "state_name": "Rio de Janeiro", "state_code": "RJ"},
    {"state_id": 20, "state_name": "Rio Grande do Norte", "state_code": "RN"},
    {"state_id": 21, "state_name": "Rio Grande do Sul", "state_code": "RS"},
    {"state_id": 22, "state_name": "Rondônia", "state_code": "RO"},
    {"state_id": 23, "state_name": "Roraima", "state_code": "RR"},
    {"state_id": 24, "state_name": "Santa Catarina", "state_code": "SC"},
    {"state_id": 25, "state_name": "São Paulo", "state_code": "SP"},
    {"state_id": 26, "state_name": "Sergipe", "state_code": "SE"},
    {"state_id": 27, "state_name": "Tocantins", "state_code": "TO"},
])

# Criar dicionário de nome normalizado → sigla
state_map = {unidecode.unidecode(row["state_name"]).lower(): row["state_code"] for _, row in states.iterrows()}
state_map.update({row["state_code"]: row["state_code"] for _, row in states.iterrows()})

# Padronizar nome de estado → sigla
customers['state'] = customers['state'].apply(lambda x: state_map.get(unidecode.unidecode(str(x)).strip().lower(), str(x)))

# Juntar com a tabela de estados para obter o state_id
customers = customers.merge(states, left_on='state', right_on='state_code', how='left')
customers.drop(columns=['state', 'state_name', 'state_code'], inplace=True)

# f) Extrair metadata da tabela web_events
def parse_metadata(meta):
    try:
        return json.loads(meta)
    except:
        return {}

metadata_expanded = web_events["metadata"].apply(parse_metadata).apply(pd.Series)
web_events = pd.concat([web_events.drop(columns=["metadata"]), metadata_expanded], axis=1)

# g) Retirar duplicidade das tabelas orders e web_events
orders = orders.drop_duplicates('order_id', keep='last')
web_events = web_events.drop_duplicates('event_id', keep='last')

# 3. Integração

# orders + customers
orders = orders.merge(customers[['id', 'email']], left_on='customer_id', right_on='id', how='left', suffixes=('', '_cust'))

# web_events + customers
web_events = web_events.merge(customers[['email']], left_on='user_email', right_on='email', how='left', suffixes=('', '_cust'))

# 4. Salvar tabelas finais
orders[['order_id', 'customer_id', 'product_code', 'order_date', 'amount','currency','order_status','payment_method']].to_csv('orders_clean.csv', index=False, date_format='%d/%m/%Y')
customers[['id', 'full_name', 'email', 'registration_date', 'state_id']].to_csv('customers_clean.csv', index=False, date_format='%d/%m/%Y')
web_events[['event_id', 'user_email', 'event_type', 'event_timestamp','page_url','page', 'referrer']].to_csv('web_events_clean.csv', index=False, date_format='%d/%m/%Y')
states.to_csv('states.csv', index=False)
