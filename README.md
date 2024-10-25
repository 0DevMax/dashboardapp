# 🏪 Sistema de Gerenciamento de Loja

Sistema web completo para gerenciamento de lojas que oferece uma experiência intuitiva no controle de vendas, estoque e visualização de relatórios.



## 📋 Índice

- [Funcionalidades](#-funcionalidades)
- [Tecnologias](#-tecnologias)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Instalação](#-instalação)
- [API](#-api)

## ✨ Funcionalidades

### Módulos Principais
- 📦 **Encomendas**: Gestão completa de pedidos
- 📝 **Catálogo**: Gerenciamento de produtos
- 📊 **Estoques**: Controle de inventário
- 💰 **Vendas**: Registro e acompanhamento
- 📈 **Relatórios**: Análises detalhadas

## 🚀 Tecnologias

### Backend
- **Flask** (Python)
- **PostgreSQL**
- **SQLAlchemy**

### Frontend
- HTML5
- CSS3
- JavaScript
- Chart.js
- DataTables

## 📁 Estrutura do Projeto

```
📦 gerenciador-de-loja/
├── 📂 app/
│   ├── 📜 app.py
│   ├── 📂 templates/
│   │   ├── 📜 dashboard.html
│   │   └── 📜 ...
│   └── 📂 static/
│       ├── 📂 css/
│       └── 📂 js/
├── 📜 requirements.txt
└── 📜 .env.example
```

## 🔧 Instalação

1. Clone o repositório
```bash
git clone https://github.com/0DevMax/dashboardapp.git
cd dashboardapp
```

2. Crie e ative um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Instale as dependências
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. Execute o aplicativo
```bash
python app.py
```

O sistema estará disponível em `http://localhost:7000`

## 🔌 API

### Endpoints Principais

| Endpoint | Método | Descrição |
|----------|---------|-----------|
| `/api/dashboard` | GET | Retorna dados do dashboard |
| `/api/catalogo` | GET | Lista produtos do catálogo |
| `/api/vendas` | GET | Dados de vendas |


## 👥 Contribuição

Contribuições são sempre bem-vindas!



Desenvolvido com ❤️ por Max
