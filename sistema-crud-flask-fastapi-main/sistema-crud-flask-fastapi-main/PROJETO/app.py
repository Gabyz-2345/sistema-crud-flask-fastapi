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

    if "estoque" not in st.session_state:

    st.session_state.estoque = {
        "Desktop Gamer": 100,
        "Headset Gamer": 100,
        "Mouse Gamer": 100,
        "Teclado Mecânico": 100
    }

if "emprestimos" not in st.session_state:

    st.session_state.emprestimos = []
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
   with col1:
    if st.button("💾 Salvar"):

        if nome.strip():

            novo_id = len(st.session_state.nomes) + 1

            st.session_state.nomes.append({
                "id": novo_id,
                "nome": nome.strip()
            })

            st.session_state.emprestimos.append({
                "nome": nome_gamer,
                "equipamento": equipamento,
                "data": str(data)
            })

            st.session_state.estoque[equipamento] -= 1

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
    if st.button("🗑 Excluir"):

        if st.session_state.selected is not None:

            nome_removido = st.session_state.nomes[st.session_state.selected]["nome"]

            for emprestimo in st.session_state.emprestimos:

                if emprestimo["nome"] == nome_removido:

                    equipamento = emprestimo["equipamento"]

                    st.session_state.estoque[equipamento] += 1

                    st.session_state.emprestimos.remove(emprestimo)

                    break

            st.session_state.nomes.pop(st.session_state.selected)

            salvar(st.session_state.nomes)

            st.session_state.selected = None

            st.rerun()

with col4:
    if st.button("Exportar CSV"):
        df = pd.DataFrame(st.session_state.nomes)
        df.to_csv("usuarios.csv", index=False)
        st.success("Arquivo CSV gerado!")

st.markdown("## 📦 Estoque Gamer")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class='card' style='border-top:5px solid #7b1fa2;'>
    <h4>🖥 Desktop</h4>
    <h2>{st.session_state.estoque['Desktop Gamer']}</h2>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class='card' style='border-top:5px solid #8e24aa;'>
    <h4>🎧 Headset</h4>
    <h2>{st.session_state.estoque['Headset Gamer']}</h2>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class='card' style='border-top:5px solid #6a1b9a;'>
    <h4>🖱 Mouse</h4>
    <h2>{st.session_state.estoque['Mouse Gamer']}</h2>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class='card' style='border-top:5px solid #4a148c;'>
    <h4>⌨ Teclado</h4>
    <h2>{st.session_state.estoque['Teclado Mecânico']}</h2>
    </div>
    """, unsafe_allow_html=True)
    
st.markdown("---")

st.markdown("## 🎮 Área Gamer")

equipamento = st.selectbox(
    "🎮 Escolha o equipamento",
    [
        "Desktop Gamer",
        "Headset Gamer",
        "Mouse Gamer",
        "Teclado Mecânico"
    ]
)

nome_gamer = st.text_input("👤 Nome da pessoa")

data = st.date_input("📅 Data do empréstimo")

g1, g2, g3, g4 = st.columns(4)

with g1:
    desktop = st.button("🖥 Desktop Gamer")

with g2:
    headset = st.button("🎧 Headset")

with g3:
    mouse = st.button("🖱 Mouse Gamer")

with g4:
    teclado = st.button("⌨ Teclado Mecânico")


if desktop:

    st.markdown("""
    <div class='card'>
    <h4>🖥 Desktop Gamer</h4>

    ✅ Disponíveis: 4<br>
    ❌ Emprestados: 2<br><br>

    👤 João — 12/05/2026<br>
    👤 Maria — 14/05/2026

    </div>
    """, unsafe_allow_html=True)


if headset:

    st.markdown("""
    <div class='card'>
    <h4>🎧 Headset Gamer</h4>

    ✅ Disponíveis: 3<br>
    ❌ Emprestados: 1<br><br>

    👤 Pedro — 15/05/2026

    </div>
    """, unsafe_allow_html=True)


if mouse:

    st.markdown("""
    <div class='card'>
    <h4>🖱 Mouse Gamer</h4>

    ✅ Disponíveis: 7<br>
    ❌ Emprestados: 0

    </div>
    """, unsafe_allow_html=True)


if teclado:

    st.markdown("""
    <div class='card'>
    <h4>⌨ Teclado Mecânico</h4>

    ✅ Disponíveis: 5<br>
    ❌ Emprestados: 1<br><br>

    👤 Ana — 10/05/2026

    </div>
    """, unsafe_allow_html=True)
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
