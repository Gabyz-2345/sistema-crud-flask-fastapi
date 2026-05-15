import streamlit as st
import json
import os
import pandas as pd

st.set_page_config(page_title="Sistema de Usuários", layout="centered")

ARQUIVO = "dados.json"


def carregar():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def salvar(dados):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)


if "nomes" not in st.session_state:
    st.session_state.nomes = carregar()

if "selected" not in st.session_state:
    st.session_state.selected = None


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

body {
    background-color: #e8f5e9;
    font-family: 'Poppins', sans-serif;
}

h1 {
    color: #1b5e20;
    text-align: center;
    font-size: 38px;
    font-weight: 700;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.12);
    margin-bottom: 20px;
}

.user {
    padding: 10px;
    margin: 6px 0;
    border-radius: 10px;
    background: #f5fff5;
    border-left: 5px solid #2e7d32;
}

.selected {
    padding: 10px;
    margin: 6px 0;
    border-radius: 10px;
    background: #c8e6c9;
    border-left: 5px solid #1b5e20;
    font-weight: bold;
}

div.stButton > button {
    border-radius: 10px;
    background-color: #2e7d32;
    color: white;
    font-weight: 600;
    width: 100%;
}

div.stButton > button:hover {
    background-color: #1b5e20;
    transform: scale(1.02);
    transition: 0.2s;
}
</style>
""", unsafe_allow_html=True)


st.title("Sistema de Cadastro de Usuários")

# ===== BUSCA =====
busca = st.text_input("🔍 Buscar usuário")

st.markdown("### Estatísticas")
st.info(f"Total de usuários: {len(st.session_state.nomes)}")

st.markdown("---")

# ===== CADASTRO =====
st.markdown("### Cadastro")

nome = st.text_input("Digite o nome do usuário")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Salvar"):
        if nome.strip():
            novo_id = len(st.session_state.nomes) + 1
            st.session_state.nomes.append({
                "id": novo_id,
                "nome": nome.strip()
            })
            salvar(st.session_state.nomes)
            st.rerun()

with col2:
    if st.button("Editar"):
        if st.session_state.selected is not None and nome.strip():
            st.session_state.nomes[st.session_state.selected]["nome"] = nome.strip()
            salvar(st.session_state.nomes)
            st.session_state.selected = None
            st.rerun()

with col3:
    if st.button("Excluir"):
        if st.session_state.selected is not None:
            st.session_state.nomes.pop(st.session_state.selected)
            salvar(st.session_state.nomes)
            st.session_state.selected = None
            st.rerun()

with col4:
    if st.button("Exportar CSV"):
        df = pd.DataFrame(st.session_state.nomes)
        df.to_csv("usuarios.csv", index=False)
        st.success("Arquivo CSV gerado!")

st.markdown("---")

# ===== LISTA =====
st.markdown("### Lista de usuários")

for i, user in enumerate(st.session_state.nomes):

    nome_user = user["nome"]
    user_id = user["id"]

    if busca and busca.lower() not in nome_user.lower():
        continue

    if st.session_state.selected == i:
        st.markdown(f"<div class='selected'>#{user_id} - 👤 {nome_user}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='user'>#{user_id} - 👤 {nome_user}</div>", unsafe_allow_html=True)

    if st.button("Selecionar", key=f"sel_{i}"):
        st.session_state.selected = i
        st.rerun()