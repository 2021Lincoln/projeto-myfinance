# 💰 MyFinance PRO - Gestão Financeira Pessoal

O **MyFinance PRO** é uma aplicação completa de controle financeiro. O sistema permite cadastrar receitas e despesas, visualizar gráficos de gastos por categoria e gerenciar o histórico de transações em tempo real.

## 🚀 Tecnologias Utilizadas

* **Frontend:** [Streamlit](https://streamlit.io/) (Interface Web interativa)
* **Backend:** [FastAPI](https://fastapi.tiangolo.com/) (API de alta performance)
* **Banco de Dados:** [SQLite](https://www.sqlite.org/) (Armazenamento relacional local)
* **Gráficos:** [Plotly](https://plotly.com/python/) (Visualização de dados)

## 🛠️ Arquitetura do Sistema

O projeto é dividido em duas partes que se comunicam via protocolo HTTP:
1.  **API (Porta 8000):** Gerencia as regras de negócio e o acesso ao banco de dados.
2.  **Dashboard (Porta 8501):** Interface onde o usuário interage com os dados.



## 📋 Como Instalar e Rodar

### 1. Clonar o repositório
```bash
git clone [https://github.com/seu-usuario/myfinance.git](https://github.com/seu-usuario/myfinance.git)
cd myfinance