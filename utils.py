import gspread
import streamlit as st
from datetime import datetime

@st.cache_resource
def get_client():
    return gspread.service_account_from_dict(
        st.secrets["google_credentials"]
    )

@st.cache_resource
def get_planilha():
    client = get_client()
    return client.open(st.secrets["SPREADSHEET_NAME"])

def get_estoque_sheet():
    return get_planilha().worksheet("ESTOQUE")

def get_historico_sheet():
    return get_planilha().worksheet("HISTÓRICO")

def listar_produtos():
    sheet = get_estoque_sheet()
    dados = sheet.get_all_records()
    return dados

def buscar_produto(codigo):
    sheet = get_estoque_sheet()
    dados = sheet.get_all_records()
    for i, row in enumerate(dados, start=2):
        if row["Código"] == codigo:
            return i, row
    return None, None

def registrar_movimentacao(tipo, codigo, quantidade):
    historico = get_historico_sheet()
    data = datetime.now().strftime("%d/%m/%Y %H:%M")

    historico.append_row([
        tipo,
        codigo,
        data,
        quantidade
    ])

def atualizar_estoque(linha, novo_valor):
    sheet = get_estoque_sheet()
    sheet.update_cell(linha, 3, novo_valor)

