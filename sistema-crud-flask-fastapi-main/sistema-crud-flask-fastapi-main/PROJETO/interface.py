import streamlit as st

st.set_page_config(page_title="CRUD Usuários", layout="centered")

if "nomes" not in st.session_state:
    st.session_state.nomes = []

if "edit_index" not in st.session_state:
    st.session_state.edit_index = None

st.markdown(
    """
    <style>
    .main {
        background-color: #e8f5e9;
    }

    div.stButton > button {
        border-radius: 12px;
        padding: 0.6em 1em;
        font-weight: bold;
        border: none;
    }

    div.stButton > button[kind="primary"] {
        background-color: #2e7d32;
        color: white;
    }

    div.stButton > button:hover {
        transform: scale(1.03);
        transition: 0.2s;
    }

    .title {
        font-size: 32px;
        font-weight: 800;
        color: #1b5e20;
        text-align: center;
    }

    .box {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='title'>📋 Cadastro de Usuários</div>", unsafe_allow_html=True)

st.markdown("<div class='box'>", unsafe_allow_html=True)

nome = st.text_input("✏️ Digite o nome do usuário")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("💾 Salvar"):
        if nome:
            st.session_state.nomes.append(nome)

with col2:
    if st.button("✏️ Editar"):
        if st.session_state.edit_index is not None and nome:
            st.session_state.nomes[st.session_state.edit_index] = nome
            st.session_state.edit_index = None

with col3:
    if st.button("🗑️ Excluir"):
        if st.session_state.edit_index is not None:
            st.session_state.nomes.pop(st.session_state.edit_index)
            st.session_state.edit_index = None

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("### 📌 Lista de usuários")

for i, n in enumerate(st.session_state.nomes):
    col1, col2 = st.columns([4, 1])

    with col1:
        st.write("👤", n)

    with col2:
        if st.button("Selecionar", key=i):
            st.session_state.edit_index = i