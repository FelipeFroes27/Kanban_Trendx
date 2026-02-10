import streamlit as st
from utils import (
    listar_produtos,
    buscar_produto,
    registrar_movimentacao,
    atualizar_estoque
)

st.set_page_config(page_title="Controle de Estoque", layout="centered")

params = st.query_params
tipo_url = params.get("tipo")

if tipo_url == "entrada":
    tipo = "Entrada"
elif tipo_url == "saida":
    tipo = "Saída"
else:
    st.warning("⚠️ Acesse o sistema pelo QR Code correto (Entrada ou Saída).")
    st.stop()

st.title(f"📦 {tipo} de Material")

produtos = listar_produtos()
codigos = [p["Código"] for p in produtos]

codigo = st.selectbox("Código do Produto", codigos)
quantidade = st.number_input("Quantidade", min_value=1, step=1)

if st.button("Registrar"):
    linha, produto = buscar_produto(codigo)

    if not produto:
        st.error("Produto não encontrado.")
        st.stop()

    estoque_atual = int(produto["Estoque atual"])

    if tipo == "Saída" and quantidade > estoque_atual:
        st.error("❌ Estoque insuficiente para essa saída.")
        st.stop()

    novo_estoque = (
        estoque_atual + quantidade
        if tipo == "Entrada"
        else estoque_atual - quantidade
    )

    registrar_movimentacao(tipo, codigo, quantidade)
    atualizar_estoque(linha, novo_estoque)

    st.success(f"✅ {tipo} registrada com sucesso!")
    st.info(f"📊 Estoque atual do produto: {novo_estoque}")

