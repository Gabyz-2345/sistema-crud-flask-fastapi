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

if "estoque" not in st.session_state:
    st.session_state.estoque = {
        "Desktop Gamer": 100,
        "Headset Gamer": 100,
        "Mouse Gamer": 100,
        "Teclado Mecânico": 100
    }

if "emprestimos" not in st.session_state:
    st.session_state.emprestimos = []


st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Poppins:wght@300;400;500;600&display=swap');

body {
    background-color: #e8f5e9;
    font-family: 'Poppins', sans-serif;
}

.title {
    font-family: 'Playfair Display', serif;
    font-size: 45px;
    text-align: center;
    color: #1b5e20;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    color: #444;
    margin-bottom: 30px;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.10);
    margin-bottom: 20px;
}

.user {
    padding: 12px;
    margin: 8px 0;
    border-radius: 12px;
    background: #f5fff5;
    border-left: 6px solid #2e7d32;
}

.selected {
    padding: 12px;
    margin: 8px 0;
    border-radius: 12px;
    background: #c8e6c9;
    border-left: 6px solid #1b5e20;
    font-weight: bold;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.10);
}

div.stButton > button {
    border-radius: 15px;
    background-color: #6a1b9a;
    color: white;
    font-weight: bold;
    border: none;
    padding: 10px;
    width: 100%;
    transition: 0.2s;
}

div.stButton > button:hover {
    background-color: #4a148c;
    transform: scale(1.03);
}

input {
    border-radius: 12px !important;
}

</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>Cadastro de Usuários</div>", unsafe_allow_html=True)

st.markdown(
    "<div class='subtitle'>Sistema Gamer de Controle e Empréstimos</div>",
    unsafe_allow_html=True
)

busca = st.text_input("🔍 Buscar usuário")

st.markdown("### 📊 Estatísticas")
st.info(f"Total de usuários cadastrados: {len(st.session_state.nomes)}")

st.markdown("---")

st.markdown("## 👤 Cadastro")

nome = st.text_input("Nome do usuário")
senha = st.text_input("Senha", type="password")

equipamento = st.selectbox(
    "🎮 Escolha o equipamento",
    [
        "Desktop Gamer",
        "Headset Gamer",
        "Mouse Gamer",
        "Teclado Mecânico"
    ]
)

data = st.date_input("📅 Data do empréstimo")

col1, col2, col3, col4 = st.columns(4)

with col1:

    if st.button("💾 Salvar"):

        if nome.strip() and senha.strip():

            if st.session_state.estoque[equipamento] > 0:

                novo_id = len(st.session_state.nomes) + 1

                st.session_state.nomes.append({
                    "id": novo_id,
                    "nome": nome.strip(),
                    "senha": senha.strip()
                })

                st.session_state.emprestimos.append({
                    "nome": nome.strip(),
                    "equipamento": equipamento,
                    "data": str(data)
                })

                st.session_state.estoque[equipamento] -= 1

                salvar(st.session_state.nomes)

                st.success("Usuário cadastrado com sucesso!")

                st.rerun()

            else:
                st.error("Equipamento indisponível.")

with col2:

    if st.button("✏️ Editar"):

        if st.session_state.selected is not None:

            if nome.strip():

                st.session_state.nomes[st.session_state.selected]["nome"] = nome.strip()

                salvar(st.session_state.nomes)

                st.success("Usuário editado!")

                st.rerun()

with col3:

    if st.button("🗑 Excluir"):

        if st.session_state.selected is not None:

            nome_removido = st.session_state.nomes[st.session_state.selected]["nome"]

            for emprestimo in st.session_state.emprestimos:

                if emprestimo["nome"] == nome_removido:

                    equipamento_removido = emprestimo["equipamento"]

                    st.session_state.estoque[equipamento_removido] += 1

                    st.session_state.emprestimos.remove(emprestimo)

                    break

            st.session_state.nomes.pop(st.session_state.selected)

            salvar(st.session_state.nomes)

            st.session_state.selected = None

            st.success("Usuário removido!")

            st.rerun()

with col4:

    if st.button("📁 Exportar CSV"):

        df = pd.DataFrame(st.session_state.nomes)

        df.to_csv("usuarios.csv", index=False)

        st.success("Arquivo CSV gerado!")

st.markdown("---")

st.markdown("## 🎮 Estoque Gamer")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class='card' style='border-top:6px solid #7b1fa2'>
    <h4>🖥 Desktop</h4>
    <h2>{st.session_state.estoque['Desktop Gamer']}</h2>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class='card' style='border-top:6px solid #8e24aa'>
    <h4>🎧 Headset</h4>
    <h2>{st.session_state.estoque['Headset Gamer']}</h2>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class='card' style='border-top:6px solid #6a1b9a'>
    <h4>🖱 Mouse</h4>
    <h2>{st.session_state.estoque['Mouse Gamer']}</h2>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class='card' style='border-top:6px solid #4a148c'>
    <h4>⌨ Teclado</h4>
    <h2>{st.session_state.estoque['Teclado Mecânico']}</h2>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("## 📋 Empréstimos")

for item in st.session_state.emprestimos:

    st.markdown(f"""
    <div class='card'>
    👤 <b>{item['nome']}</b><br><br>
    🎮 Equipamento: {item['equipamento']}<br>
    📅 Data: {item['data']}
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("## 👥 Lista de usuários")

for i, user in enumerate(st.session_state.nomes):

    nome_user = user["nome"]
    user_id = user["id"]

    if busca and busca.lower() not in nome_user.lower():
        continue

    if st.session_state.selected == i:

        st.markdown(
            f"<div class='selected'>#{user_id} - 👤 {nome_user}</div>",
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"<div class='user'>#{user_id} - 👤 {nome_user}</div>",
            unsafe_allow_html=True
        )

    if st.button("Selecionar", key=f"sel_{i}"):

        st.session_state.selected = i

        st.rerun()
