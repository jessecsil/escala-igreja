import streamlit as st
import pandas as pd
import urllib.parse
from fpdf import FPDF

# --- CONFIGURAÇÃO DO APP ---
st.set_page_config(page_title="Escala Igreja", layout="wide", page_icon="🎵")

# Inicialização da equipe
if 'equipe' not in st.session_state:
    st.session_state.equipe = {
        "Som": ["Jessé", "Junior", "Paulo", "Marcelo"],
        "Transmissão": ["Mel", "Arthur", "Pedro", "Junior", "Cláudia", "Jessé"],
        "Mídia": ["Cláudia", "Sophia", "Gabriela", "Pedro", "Junior", "Jessé"],
        "Equipe": ["Bruna", "Fernanda", "Junior", "Jovens"]
    }

def com_opcao_vazia(lista):
    return ["-"] + lista

# --- TÍTULO DO SISTEMA ---
st.markdown("### 🎵 Sistema de Escala - Som | Transmissão | Mídia")

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

c_tit, c_sel, c_vazio = st.columns([0.4, 0.4, 1.2])
with c_tit:
    st.markdown('<p style="font-size: 16px; font-weight: bold; margin-top: 10px;">🗓️ Equipe da Semana:</p>', unsafe_allow_html=True)

with c_sel:
    e_geral = st.selectbox("", com_opcao_vazia(st.session_state.equipe["Equipe"]), label_visibility="collapsed")

st.divider()

c1, c2, c3 = st.columns(3)
with c1:
    st.info("📅 Ensaio")
    s_sex = st.selectbox("Som", com_opcao_vazia(st.session_state.equipe["Som"]), key="s_sex")
with c2:
    st.success("☀️ Domingo Manhã")
    s_dom_m = st.selectbox("Som", com_opcao_vazia(st.session_state.equipe["Som"]), key="sm")
    t_dom_m = st.selectbox("Transmissão", com_opcao_vazia(st.session_state.equipe["Transmissão"]), key="tm")
    m_dom_m = st.selectbox("Mídia", com_opcao_vazia(st.session_state.equipe["Mídia"]), key="mm")
with c3:
    st.success("🌙 Domingo Noite")
    s_dom_n = st.selectbox("Som", com_opcao_vazia(st.session_state.equipe["Som"]), key="sn")
    t_dom_n = st.selectbox("Transmissão", com_opcao_vazia(st.session_state.equipe["Transmissão"]), key="tn")
    m_dom_n = st.selectbox("Mídia", com_opcao_vazia(st.session_state.equipe["Mídia"]), key="mn")

# --- GERAÇÃO DA TABELA E AÇÕES ---
st.divider()
if st.button("✅ Confirmar e Gerar Tabela"):
    if e_geral != "-":
        st.markdown(f"#### Equipe: **{e_geral}**")
        
    dados = {
        "Período": ["Ensaio", "Dom. Manhã", "Dom. Noite"],
        "Som": [s_sex, s_dom_m, s_dom_n],
        "Transmissão": ["-", t_dom_m, t_dom_n],
        "Mídia": ["-", m_dom_m, m_dom_n]
    }
    df = pd.DataFrame(dados)
    st.table(df)

    st.write("---")
    col_w, col_p = st.columns(2)

    with col_w:
        # WHATSAPP
        texto_whatsapp = f"🎵 *ESCALA MÍDIA E SOM* 🎵\n\n"
        if e_geral != "-": texto_whatsapp += f"⭐ *Equipe:* {e_geral}\n\n"
        texto_whatsapp += f"📅 *Ensaio*\n- Som: {s_sex}\n\n"
        texto_whatsapp += f"☀️ *Domingo Manhã*\n- Som: {s_dom_m}\n- Transmissão: {t_dom_m}\n- Mídia: {m_dom_m}\n\n"
        texto_whatsapp += f"🌙 *Domingo Noite*\n- Som: {s_dom_n}\n- Transmissão: {t_dom_n}\n- Mídia: {m_dom_n}"
        link_zap = f"https://wa.me/?text={urllib.parse.quote(texto_whatsapp)}"
        st.markdown(f'<a href="{link_zap}" target="_blank"><button style="background-color: #25D366; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-weight: bold; width: 100%;">📲 Enviar WhatsApp</button></a>', unsafe_allow_html=True)

    with col_p:
        # GERAR PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(190, 10, "ESCALA DE LOUVOR E MIDIA", ln=True, align="C")
        pdf.ln(5)
        if e_geral != "-":
            pdf.set_font("Arial", "B", 12)
            pdf.cell(190, 10, f"Equipe: {e_geral}", ln=True, align="C")
        pdf.ln(10)
        
        # Cabeçalho da Tabela no PDF
        pdf.set_fill_color(200, 200, 200)
        pdf.set_font("Arial", "B", 10)
        cols = ["Periodo", "Som", "Transm.", "Midia"]
        for col in cols:
            pdf.cell(47.5, 10, col, border=1, align="C", fill=True)
        pdf.ln()

        # Dados da Tabela no PDF
        pdf.set_font("Arial", "", 10)
        for i in range(len(df)):
            pdf.cell(47.5, 10, str(df.iloc[i,0]), border=1, align="C")
            pdf.cell(47.5, 10, str(df.iloc[i,1]), border=1, align="C")
            pdf.cell(47.5, 10, str(df.iloc[i,2]), border=1, align="C")
            pdf.cell(47.5, 10, str(df.iloc[i,3]), border=1, align="C")
            pdf.ln()

        pdf_output = pdf.output(dest='S').encode('latin-1')
        st.download_button(
            label="💾 Baixar Escala (PDF)",
            data=pdf_output,
            file_name=f"Escala_{e_geral}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
