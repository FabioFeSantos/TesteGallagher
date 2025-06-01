# Diagrama de Entidades – v1

![Diagrama de Entidades](diagrama-entidades.png)

## Entidades e Atributos

| Tabela     | Chave Primária | Chaves Estrangeiras | Atributos                                                        | Descrição                        |
|------------|---------------|---------------------|-------------------------------------------------------------------|----------------------------------|
| customers  | customer_id   | state_id            | full_name, email (unique), registration_date, birth_date, phone_number, customer_segment | Clientes do sistema              |
| orders     | order_id      | customer_id         | product_code, order_date, amount                                  | Pedidos realizados pelos clientes|
| web_events | event_id      | customer_id         | event_type, event_timestamp, device, browser, source              | Eventos de navegação dos clientes|
| states     | state_id      | -                   | name, code                                                        | Estados/regiões dos clientes     |

## Relacionamentos

- `customers.state_id` → `states.state_id`: Cada cliente pertence a um estado.
- `orders.customer_id` → `customers.customer_id`: Cada pedido é feito por um cliente.
- `web_events.customer_id` → `customers.customer_id`: Cada evento de navegação está associado a um cliente.

## Histórico de versões

- **v1**: Estrutura inicial do modelo de dados.

---

> Para criar uma nova versão, copie a pasta `v1` para `v2`, atualize o diagrama e a documentação conforme necessário e faça um commit com uma mensagem clara, por exemplo:  
> `docs(erd): adiciona versão v2 do diagrama de entidades`
