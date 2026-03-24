import streamlit as st
import pandas as pd
import urllib.parse
from fpdf import FPDF

# --- CONFIGURAÇÃO DO APP ---
st.set_page_config(page_title="Escala Igreja", layout="wide", page_icon="🎵")

# --- LISTA DEFINITIVA DA EQUIPE ---
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

# --- BARRA LATERAL ---
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
c_tit, c_sel, c_espaco = st.columns([0.18, 0.25, 0.57])
with c_tit:
    st.markdown('<p style="font-size: 16px; font-weight: bold; margin-top: 10px; white-space: nowrap;">🗓️ Equipe da Semana:</p>', unsafe_allow_html=True)
with c_sel:
    e_geral = st.selectbox("", com_opcao_vazia(st.session_state.equipe["Equipe"]), label_visibility="collapsed")

st.divider()

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
    
    # Criamos os dados brutos
    dados = [
        {"Periodo": "Ensaio", "Som": s_ens, "Transmissao": "-", "Midia": "-"},
        {"Periodo": "Domingo Manha", "Som": s_dom_m, "Transmissao": t_dom_m, "Midia": m_dom_m},
        {"Periodo": "Domingo Noite", "Som": s_dom_n, "Transmissao": t_dom_n, "Midia": m_dom_n},
        {"Periodo": "Evento", "Som": s_evt, "Transmissao": t_evt, "Midia": m_evt}
    ]
    
    # FILTRO: Só mantém o período se pelo menos um dos campos (Som, Transmissão ou Mídia) for diferente de "-"
    dados_filtrados = [d for d in dados if d["Som"] != "-" or d["Transmissao"] != "-" or d["Midia"] != "-"]
    
    if not dados_filtrados:
        st.warning("Nenhum integrante selecionado para a escala.")
    else:
        df = pd.DataFrame(dados_filtrados)
        st.table(df)

        st.write("---")
        col_w, col_p = st.columns(2)

        with col_w:
            # WHATSAPP DINÂMICO (Só mostra o que foi preenchido)
            txt = "ESCALA SOM | MIDIA | TRANSMISSAO\n\n"
            if e_geral != "-": txt += f"Equipe: {e_geral}\n\n"
            
            for item in dados_filtrados:
                txt += f"{item['Periodo'].upper()}\n"
                if item['Som'] != "-": txt += f"- Som: {item['Som']}\n"
                if item['Transmissao'] != "-": txt += f"- Transmissao: {item['Transmissao']}\n"
                if item['Midia'] != "-": txt += f"- Midia: {item['Midia']}\n"
                txt += "\n"
            
            link_zap = f"https://wa.me/?text={urllib.parse.quote(txt)}"
            st.markdown(f'<a href="{link_zap}" target="_blank"><button style="background-color: #25D366; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-weight: bold; width: 100%;">📲 Enviar WhatsApp</button></a>', unsafe_allow_html=True)

        with col_p:
            # --- PDF DINÂMICO ---
            pdf = FPDF(format=(150, 110))
            pdf.add_page()
            pdf.set_font("Arial", "B", 14)
            titulo_pdf = "ESCALA SOM | MIDIA | TRANSMISSAO".encode('latin-1', 'replace').decode('latin-1')
            pdf.cell(130, 8, titulo_pdf, ln=True, align="C")
            pdf.ln(5)
            
            # Cabeçalho
            pdf.set_fill_color(230, 230, 230)
            pdf.set_font("Arial", "B", 9)
            pdf.cell(35, 8, "Periodo", 1, 0, "C", True)
            pdf.cell(30, 8, "Som", 1, 0, "C", True)
            pdf.cell(30, 8, "Midia", 1, 0, "C", True)
            pdf.cell(35, 8, "Transmissao", 1, 1, "C", True)

            # Dados (Só os filtrados)
            pdf.set_font("Arial", "", 9)
            for _, row in df.iterrows():
                pdf.cell(35, 8, str(row['Periodo']).encode('latin-1', 'replace').decode('latin-1'), 1, 0, "C")
                pdf.cell(30, 8, str(row['Som']).encode('latin-1', 'replace').decode('latin-1'), 1, 0, "C")
                pdf.cell(30, 8, str(row['Midia']).encode('latin-1', 'replace').decode('latin-1'), 1, 0, "C")
                pdf.cell(35, 8, str(row['Transmissao']).encode('latin-1', 'replace').decode('latin-1'), 1, 1, "C")

            pdf_bin = pdf.output(dest='S').encode('latin-1', 'replace')
            st.download_button(label="💾 Baixar Escala (PDF)", data=pdf_bin, file_name=f"Escala_{e_geral}.pdf", mime="application/pdf", use_container_width=True)
