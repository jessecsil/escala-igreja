import streamlit as st
import pandas as pd
import urllib.parse
from fpdf import FPDF

# --- CONFIGURAÇÃO DO APP ---
st.set_page_config(page_title="Escala Igreja", layout="wide", page_icon="🎵")

# --- LISTA DEFINITIVA DA EQUIPE (ATUALIZADA) ---
if 'equipe' not in st.session_state:
    st.session_state.equipe = {
        "Som": ["Marcelo", "Jessé", "Junior", "Paulo"],
        "Transmissão": ["Mel", "Pedro", "Jessé", "Junior", "Arthur", "Cláudia"],
        "Mídia": ["Cláudia", "Sophia", "Gabriela", "Pedro", "Jessé", "Junior"],
        "Equipe": ["Bruna", "Junior", "Fernanda", "Cláudia", "Jovens"]
    }

def com_opcao_vazia(lista):
    return ["-"] + lista

# --- TÍTULO DO SISTEMA ---
st.markdown("### 🎵 Escala Som | Mídia | Transmissão")

# --- BARRA LATERAL (GERENCIAMENTO) ---
with st.sidebar:
    st.header("⚙️ Gerenciar Equipe")
    cat_add = st.selectbox("Área para Adicionar", ["Som", "Transmissão", "Mídia", "Equipe"], key="add_cat")
    nome_add = st.text_input("Nome do Integrante", key="add_nome")
    if st.button("➕ Adicionar"):
        if nome_add:
            st.session_state.equipe[cat_add].append(nome_add)
            st.rerun()
    st.divider()
    cat_rem = st.selectbox("Área para Remover", ["Som", "Transmissão", "Mídia", "Equipe"], key="rem_cat")
    nome_rem = st.selectbox("Selecionar Nome para Excluir", st.session_state.equipe[cat_rem], key="rem_nome")
    if st.button("🗑️ Excluir Nome"):
        st.session_state.equipe[cat_rem].remove(nome_rem)
        st.rerun()

# --- MONTAGEM DA ESCALA ---
st.write("") 

# Ajuste de Proximidade da Equipe
c_tit, c_sel, c_espaco = st.columns([0.18, 0.25, 0.57])
with c_tit:
    st.markdown('<p style="font-size: 16px; font-weight: bold; margin-top: 10px; white-space: nowrap;">🗓️ Equipe da Semana:</p>', unsafe_allow_html=True)
with c_sel:
    e_geral = st.selectbox("", com_opcao_vazia(st.session_state.equipe["Equipe"]), label_visibility="collapsed")

st.divider()

# Layout de 4 colunas
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.info("📅 Ensaio")
    s_ens = st.selectbox("Som", com_opcao_vazia(st.session_state.equipe["Som"]), key="s_ens_val")
with c2:
    st.success("☀️ Domingo Manhã")
    s_dom_m = st.selectbox("Som", com_opcao_vazia(st.session_state.equipe["Som"]), key="sm_val")
    t_dom_m = st.selectbox("Transmissão", com_opcao_vazia(st.session_state.equipe["Transmissão"]), key="tm_val")
    m_dom_m = st.selectbox("Mídia", com_opcao_vazia(st.session_state.equipe["Mídia"]), key="mm_val")
with c3:
    st.success("🌙 Domingo Noite")
    s_dom_n = st.selectbox("Som", com_opcao_vazia(st.session_state.equipe["Som"]), key="sn_val")
    t_dom_n = st.selectbox("Transmissão", com_opcao_vazia(st.session_state.equipe["Transmissão"]), key="tn_val")
    m_dom_n = st.selectbox("Mídia", com_opcao_vazia(st.session_state.equipe["Mídia"]), key="mn_val")
with c4:
    st.warning("✨ Evento")
    s_evt = st.selectbox("Som", com_opcao_vazia(st.session_state.equipe["Som"]), key="se_val")
    t_evt = st.selectbox("Transmissão", com_opcao_vazia(st.session_state.equipe["Transmissão"]), key="te_val")
    m_evt = st.selectbox("Mídia", com_opcao_vazia(st.session_state.equipe["Mídia"]), key="me_val")

# --- GERAÇÃO DA TABELA E AÇÕES ---
st.divider()
if st.button("✅ Confirmar e Gerar Tabela"):
    if e_geral != "-":
        st.markdown(f"#### Equipe: **{e_geral}**")
        
    dados = {
        "Período": ["Ensaio", "Domingo Manhã", "Domingo Noite", "Evento"],
        "Som": [s_ens, s_dom_m, s_dom_n, s_evt],
        "Transmissão": ["-", t_dom_m, t_dom_n, t_evt],
        "Mídia": ["-", m_dom_m, m_dom_n, m_evt]
    }
    df = pd.DataFrame(dados)
    st.table(df)

    st.write("---")
    col_w, col_p = st.columns(2)

    with col_w:
        # WHATSAPP (Texto limpo para evitar símbolos estranhos)
        txt = "ESCALA SOM | MIDIA | TRANSMISSAO\n\n"
        if e_geral != "-": txt += f"Equipe: {e_geral}\n\n"
        txt += f"ENSAIO\n- Som: {s_ens}\n\n"
        txt += f"DOMINGO MANHA\n- Som: {s_dom_m}\n- Transmissao: {t_dom_m}\n- Midia: {m_dom_m}\n\n"
        txt += f"DOMINGO NOITE\n- Som: {s_dom_n}\n- Transmissao: {t_dom_n}\n- Midia: {m_dom_n}\n\n"
        txt += f"EVENTO\n- Som: {s_evt}\n- Transmissao: {t_evt}\n- Midia: {m_evt}"
        
        link_zap = f"https://wa.me/?text={urllib.parse.quote(txt)}"
        st.markdown(f'<a href="{link_zap}" target="_blank"><button style="background-color: #25D366; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-weight: bold; width: 100%;">📲 Enviar WhatsApp</button></a>', unsafe_allow_html=True)

    with col_p:
        # --- PDF PERSONALIZADO ---
        pdf = FPDF(format=(150, 110))
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        
        titulo_pdf = "ESCALA SOM | MIDIA | TRANSMISSAO".encode('latin-1', 'replace').decode('latin-1')
        pdf.cell(130, 8, titulo_pdf, ln=True, align="C")
        
        pdf.ln(3)
        if e_geral != "-":
            pdf.set_font("Arial", "B", 11)
            equipe_txt = f"Equipe: {e_geral}".encode('latin-1', 'replace').decode('latin-1')
            pdf.cell(130, 8, equipe_txt, ln=True, align="C")
        pdf.ln(5)
        
        # Cabeçalho da Tabela
        pdf.set_fill_color(230, 230, 230)
        pdf.set_font("Arial", "B", 9)
        cols_pdf = [("Periodo", 35), ("Som", 30), ("Midia", 30), ("Transmissao", 35)]
        
        for col_name, width in cols_pdf:
            txt_col = col_name.encode('latin-1', 'replace').decode('latin-1')
            pdf.cell(width, 8, txt_col, border=1, align="C", fill=True)
        pdf.ln()

        # Dados da Tabela
        pdf.set_font("Arial", "", 9)
        for i in range(len(df)):
            pdf.cell(35, 8, str(df.iloc[i,0]).encode('latin-1', 'replace').decode('latin-1'), border=1, align="C")
            pdf.cell(30, 8, str(df.iloc[i,1]).encode('latin-1', 'replace').decode('latin-1'), border=1, align="C")
            pdf.cell(30
