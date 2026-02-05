# Lead Management API

API para gerenciamento de Leads desenvolvida com Python, FastAPI e MongoDB.

## 🚀 Tecnologias

- **Python 3.11**
- **FastAPI**: Framework web moderno e rápido.
- **MongoDB**: Banco de dados NoSQL.
- **Motor**: Driver assíncrono para MongoDB.
- **Docker**: Containerização da aplicação.

## 📂 Estrutura do Projeto

A arquitetura segue o padrão de separação de responsabilidades (Clean Architecture simplificada):

- **app/routers**: Definição das rotas e endpoints da API.
- **app/services**: Regras de negócio e integração com serviços externos.
- **app/schemas**: Modelos Pydantic para validação de dados (DTOs).
- **app/models**: Definições de modelos (embora o MongoDB seja schemaless, mantemos a estrutura lógica aqui).
- **app/database**: Configuração e conexão com o banco de dados.
- **app/core**: Configurações globais e variáveis de ambiente.

## 🛠️ Como Rodar o Projeto

### Opção 1: Docker (Recomendado)

Certifique-se de ter o Docker e Docker Compose instalados.

1. Execute o comando na raiz do projeto:
   ```bash
   docker-compose up --build
   ```

2. A API estará disponível em: `http://localhost:8000`

### Opção 2: Localmente

1. Crie um ambiente virtual e instale as dependências:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```

2. Tenha uma instância do MongoDB rodando localmente na porta `27017` ou configure a variável de ambiente `MONGO_URL` no arquivo `.env`.

3. Execute a aplicação:
   ```bash
   uvicorn app.main:app --reload
   ```

## 🧪 Testando Manualmente os Endpoints

Você pode usar a documentação interativa do FastAPI em `http://localhost:8000/docs` ou usar o `curl`.

### 1. Criar um Lead (POST /leads)

```bash
curl -X 'POST' \
  'http://localhost:8000/leads' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "João Silva",
  "email": "joao@example.com",
  "phone": "+5511999999999"
}'
```

**Comportamento esperado**: O sistema irá consultar a API externa (`dummyjson.com`), obter a data de nascimento e salvar o lead.

### 2. Listar Leads (GET /leads)

```bash
curl -X 'GET' \
  'http://localhost:8000/leads' \
  -H 'accept: application/json'
```

### 3. Obter Lead por ID (GET /leads/{id})

Substitua `{id}` pelo ID retornado na criação.

```bash
curl -X 'GET' \
  'http://localhost:8000/leads/65c1234567890abcdef12345' \
  -H 'accept: application/json'
```

## ⚠️ Integração Externa e Tratamento de Falhas

Durante a criação do lead, a API consulta o serviço `https://dummyjson.com/users/1` para obter o campo `birthDate`.

**Estratégia de Falha**:
Caso a API externa esteja indisponível ou retorne erro:
- O erro é logado no servidor.
- O campo `birth_date` será salvo como `null` no banco de dados.
- A criação do lead **não** é interrompida, garantindo que o dado principal (contato) seja preservado.

Isso garante resiliência à aplicação, evitando que instabilidades de terceiros impactem o fluxo principal de cadastro.
