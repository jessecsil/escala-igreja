import streamlit as st
import pandas as pd
import urllib.parse
from fpdf import FPDF

# --- CONFIGURAÇÃO DO APP ---
st.set_page_config(page_title="Escala Igreja", layout="wide", page_icon="🎵")

# --- LISTA DA EQUIPE ---
if 'equipe' not in st.session_state:
    st.session_state.equipe = {
        "Som": ["Marcelo", "Jessé", "Junior", "Paulo"],
        "Transmissão": ["Mel", "Pedro", "Jessé", "Junior", "Arthur", "Cláudia"],
        "Mídia": ["Cláudia", "Sophia", "Gabriela", "Pedro", "Jessé", "Junior"],
        "Equipe": ["Bruna", "Junior", "Fernanda", "Cláudia", "Jovens"]
    }

def com_opcao_vazia(lista):
    return ["-"] + lista

# --- TÍTULO ---
st.markdown("### 🎵 Escala Som | Mídia | Transmissão")

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("⚙️ Gerenciar Equipe")
    cat_add = st.selectbox("Área", ["Som", "Transmissão", "Mídia", "Equipe"])
    nome_add = st.text_input("Nome")
    if st.button("➕ Adicionar"):
        if nome_add:
            st.session_state.equipe[cat_add].append(nome_add)
            st.rerun()
    st.divider()
    cat_rem = st.selectbox("Remover de", ["Som", "Transmissão", "Mídia", "Equipe"])
    nome_rem = st.selectbox("Nome para Excluir", st.session_state.equipe[cat_rem])
    if st.button("🗑️ Excluir"):
        st.session_state.equipe[cat_rem].remove(nome_rem)
        st.rerun()

# --- MONTAGEM ---
st.write("") 
c_tit, c_sel, c_esp = st.columns([0.18, 0.25, 0.57])
with c_tit:
    st.markdown('<p style="font-weight: bold; margin-top: 10px;">🗓️ Equipe:</p>', unsafe_allow_html=True)
with c_sel:
    e_geral = st.selectbox("", com_opcao_vazia(st.session_state.equipe["Equipe"]), label_visibility="collapsed")

st.divider()

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.info("📅 Ensaio")
    s_ens = st.selectbox("Som", com_opcao_vazia(st.session_state.equipe["Som"]), key="s1")
with c2:
    st.success("☀️ Domingo Manhã")
    s_dm = st.selectbox("Som", com_opcao_vazia(st.session_state.equipe["Som"]), key="s2")
    t_dm = st.selectbox("Transmissão", com_opcao_vazia(st.session_state.equipe["Transmissão"]), key="t2")
    m_dm = st.selectbox("Mídia", com_opcao_vazia(st.session_state.equipe["Mídia"]), key="m2")
with c3:
    st.success("🌙 Domingo Noite")
    s_dn = st.selectbox("Som", com_opcao_vazia(st.session_state.equipe["Som"]), key="s3")
    t_dn = st.selectbox("Transmissão", com_opcao_vazia(st.session_state.equipe["Transmissão"]), key="t3")
    m_dn = st.selectbox("Mídia", com_opcao_vazia(st.session_state.equipe["Mídia"]), key="m3")
with c4:
    st.warning("✨ Evento")
    s_ev = st.selectbox("Som", com_opcao_vazia(st.session_state.equipe["Som"]), key="s4")
    t_ev = st.selectbox("Transmissão", com_opcao_vazia(st.session_state.equipe["Transmissão"]), key="t4")
    m_ev = st.selectbox("Mídia", com_opcao_vazia(st.session_state.equipe["Mídia"]), key="m4")

# --- GERAÇÃO DA TABELA ---
st.divider()
if st.button("✅ Confirmar e Gerar Tabela"):
    dados = [
        {"Período": "Ensaio", "Som": s_ens, "Transmissão": "-", "Mídia": "-"},
        {"Período": "Domingo Manhã", "Som": s_dm, "Transmissão": t_dm, "Mídia": m_dm},
        {"Período": "Domingo Noite", "Som": s_dn, "Transmissão": t_dn, "Mídia": m_dn},
        {"Período": "Evento", "Som": s_ev, "Transmissão": t_ev, "Mídia": m_ev}
    ]
    
    filtrados = [d for d in dados if d["Som"] != "-" or d["Transmissão"] != "-" or d["Mídia"] != "-"]
    
    if filtrados:
        df = pd.DataFrame(filtrados)
        st.table(df)

        st.write("---")
        col_w, col_p = st.columns(2)

        with col_w:
            # WHATSAPP: Removi os emojis complexos do início para evitar a "?" 
            # Usei apenas símbolos básicos que o WhatsApp entende 100%
            txt = "*ESCALA SOM | MIDIA | TRANSMISSAO*\n\n"
            if e_geral != "-": txt += f"Equipe: *{e_geral}*\n\n"
            
            for item in filtrados:
                # Removemos o acento apenas na variável do texto do WhatsApp para garantir
                periodo_limpo = item['Período'].replace("ã", "a").replace("í", "i")
                txt += f"*{periodo_limpo.upper()}*\n"
                if item['Som'] != "-": txt += f"  Som: {item['Som']}\n"
                if item['Transmissão'] != "-": txt += f"  Transmissao: {item['Transmissão']}\n"
                if item['Mídia'] != "-": txt += f"  Midia: {item['Mídia']}\n"
                txt += "\n"
            
            # Codificação segura
            link = f"https://wa.me/?text={urllib.parse.quote(txt.encode('utf-8'))}"
            st.markdown(f'<a href="{link}" target="_blank"><button style="background-color: #25D366; color: white; border: none; padding: 10px 20px; border-radius: 5px; font-weight: bold; width: 100%;">📲 Enviar WhatsApp</button></a>', unsafe_allow_html=True)

        with col_p:
            # PDF (Mantido com correção para acentos)
            pdf = FPDF(format=(150, 110))
            pdf.add_page()
            pdf.set_font("Arial", "B", 14)
            
            def fix_txt(t):
                return str(t).encode('windows-1252', 'replace').decode('windows-1252')

            pdf.cell(130, 8, fix_txt("ESCALA SOM | MÍDIA | TRANSMISSÃO"), ln=True, align="C")
            if e_geral != "-":
                pdf.set_font("Arial", "B", 11)
                pdf.cell(130, 8, fix_txt(f"Equipe: {e_geral}"), ln=True, align="C")
            pdf.ln(5)
            
            pdf.set_fill_color(230, 230, 230)
            pdf.set_font("Arial", "B", 9)
            pdf.cell(35, 8, fix_txt("Período"), 1, 0, "C", True)
            pdf.cell(30, 8, "Som", 1, 0, "C", True)
            pdf.cell(30, 8, fix_txt("Mídia"), 1, 0, "C", True)
            pdf.cell(35, 8, fix_txt("Transmissão"), 1, 1, "C", True)

            pdf.set_font("Arial", "", 9)
            for _, row in df.iterrows():
                pdf.cell(35, 8, fix_txt(row['Período']), 1, 0, "C")
                pdf.cell(30, 8, fix_txt(row['Som']), 1, 0, "C")
                pdf.cell(30, 8, fix_txt(row['Mídia']), 1, 0
