import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import time
import os

st.set_page_config(page_title="MyFinance PRO", page_icon="💰", layout="wide")

# --- GERENCIAMENTO DE CATEGORIAS (PERSISTÊNCIA LOCAL) ---
ARQUIVO_CAT = "categorias.txt"

def carregar_categorias():
    categorias_padrao = [
        "Salário", "Alimentação", "Lazer", "Saúde", "Aluguel", "imprevistos", 
        "Despesas Fixas", "Internet", "Telefone", "Cartão", "Agua", "Luz", "Obras", 
        "Pensão", "Cartão Daniele", "Cartão Lincoln","Transporte", "Combustivel", 
        "Educação", "Investimentos", "Supermercado", "Outros"
    ]
    
    # Se o arquivo não existir, cria ele com as categorias padrão
    if not os.path.exists(ARQUIVO_CAT):
        with open(ARQUIVO_CAT, "w", encoding="utf-8") as f:
            for c in categorias_padrao:
                f.write(c + "\n")
        return sorted(categorias_padrao)
    
    # Se o arquivo existir, lê o que está lá
    with open(ARQUIVO_CAT, "r", encoding="utf-8") as f:
        categorias_no_arquivo = [line.strip() for line in f.readlines() if line.strip()]
    
    # Garante que as padrão sempre estejam na lista, sem duplicar
    lista_final = list(set(categorias_padrao + categorias_no_arquivo))
    return sorted(lista_final)

def salvar_categoria(nova_cat):
    categorias = carregar_categorias()
    if nova_cat not in categorias:
        with open(ARQUIVO_CAT, "a", encoding="utf-8") as f:
            f.write(nova_cat + "\n")
        return True
    return False

# --- FUNÇÃO COM CACHE ---
@st.cache_data(ttl=60)
def carregar_dados_servidor():
    try:
        response = requests.get("http://localhost:8000/transacoes/", timeout=3)
        if response.status_code == 200:
            return response.json()
    except:
        return None
    return None

st.title("💰 Minhas finanças - Gestão Financeira")

# --- SIDEBAR: CADASTRO E CATEGORIAS ---
st.sidebar.header("Nova Transação")
desc = st.sidebar.text_input("Descrição")
val = st.sidebar.number_input("Valor", min_value=0.0, step=10.0)
tp = st.sidebar.selectbox("Tipo", ["Receita", "Despesa"])

# Carrega as categorias do arquivo
lista_categorias = carregar_categorias()
cat = st.sidebar.selectbox("Categoria", lista_categorias)

dt = st.sidebar.date_input("Data")

if st.sidebar.button("Salvar Transação", use_container_width=True):
    if desc:
        dados = {"descricao": desc, "valor": val, "tipo": tp, "categoria": cat, "data": str(dt)}
        try:
            res = requests.post("http://localhost:8000/transacoes/", json=dados)
            if res.status_code == 200:
                st.sidebar.success("Salvo!")
                st.cache_data.clear()
                time.sleep(0.5)
                st.rerun()
        except:
            st.sidebar.error("Backend Offline")

st.sidebar.divider()
st.sidebar.header("⚙️ Configurações")

# Interface para criar nova categoria
with st.sidebar.expander("➕ Criar Nova Categoria"):
    nova_cat_input = st.text_input("Nome da categoria")
    if st.button("Adicionar Categoria"):
        if nova_cat_input:
            if salvar_categoria(nova_cat_input):
                st.success("Criada!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.warning("Já existe!")
        else:
            st.error("Digite um nome!")

# --- PROCESSAMENTO DE DADOS ---
dados_brutos = carregar_dados_servidor()
df = pd.DataFrame(dados_brutos) if dados_brutos else pd.DataFrame()

if not df.empty:
    df['valor'] = pd.to_numeric(df['valor'])
    df['data'] = pd.to_datetime(df['data'])

    total_receitas = df[df['tipo'] == 'Receita']['valor'].sum()
    total_despesas = df[df['tipo'] == 'Despesa']['valor'].sum()
    saldo_atual = total_receitas - total_despesas

    # --- MÉTRICAS ---
    c1, c2, c3 = st.columns(3)
    c1.metric("Total de Entradas", f"R$ {total_receitas:.2f}")
    c2.metric("Total de Despesas", f"R$ {total_despesas:.2f}")
    c3.metric("Saldo Atual", f"R$ {saldo_atual:.2f}", delta=f"{saldo_atual:.2f}")

    st.divider()

    # --- DASHBOARD ---
    col_hist, col_graf = st.columns([1.5, 1])

    with col_hist:
        st.subheader("🔍 Histórico Recente")
        filtro_cat = st.selectbox("Filtrar Categoria", ["Todas"] + lista_categorias)
        
        df_view = df.copy()
        if filtro_cat != "Todas":
            df_view = df_view[df_view['categoria'] == filtro_cat]
        
        df_view['data'] = df_view['data'].dt.strftime('%d/%m/%Y')
        st.dataframe(df_view.sort_values('id', ascending=False), use_container_width=True, hide_index=True)

    with col_graf:
        st.subheader("📊 Gastos por Categoria")
        df_gastos = df[df['tipo'] == 'Despesa']
        if not df_gastos.empty:
            fig = px.pie(df_gastos, values='valor', names='categoria', hole=0.4,
                         color_discrete_sequence=px.colors.qualitative.Pastel)
            fig.update_traces(textinfo='percent+value')
            st.plotly_chart(fig, use_container_width=True)

    # --- EXCLUSÃO ---
    with st.expander("🗑️ Gerenciar Registros"):
        opcoes = {f"ID {r.id} | {r.descricao} (R$ {r.valor:.2f})": r.id for r in df.itertuples()}
        selecionado = st.selectbox("Escolha para deletar:", list(opcoes.keys()))
        
        if st.button("Confirmar Exclusão", type="primary"):
            requests.delete(f"http://localhost:8000/transacoes/{opcoes[selecionado]}")
            st.cache_data.clear()
            st.rerun()
else:
    st.info("Nenhum dado encontrado. O Backend está rodando?")