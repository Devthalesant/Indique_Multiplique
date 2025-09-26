import streamlit as st
from Functions.treating_bases import *
import pandas as pd
from io import BytesIO

# Configuração da página
st.set_page_config(
    page_title="Indique & Multiplique",
    page_icon="✨",
    layout="wide"
)

# CSS personalizado
st.markdown("""
<style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 24px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
        color: white;
    }
    .stDownloadButton>button {
        background-color: #2196F3;
        color: white;
        border-radius: 5px;
        padding: 10px 24px;
        font-weight: bold;
    }
    .stDownloadButton>button:hover {
        background-color: #0b7dda;
        color: white;
    }
    .header {
        color: #2c3e50;
        text-align: center;
    }
    .success-msg {
        color: #4CAF50;
        font-weight: bold;
    }
    .footer {
        text-align: center;
        color: #555;
        font-size: 14px;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Título com emojis
st.markdown('<h1 class="header">📊 Campanha Indique & Multiplique 💰</h1>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar com informações
with st.sidebar:
    st.header("ℹ️ Informações")
    st.markdown("""
    **Como usar:**
    1. Faça upload das planilhas necessárias
    2. Os dados serão processados automaticamente
    3. Visualize os resultados
    4. Baixe a planilha consolidada
    """)
    st.markdown("---")
    st.markdown("""
    <style>
        .footer {
            text-align: center;
            background-color: #2c3e50;
            color: white;
            padding: 10px;
            border-radius: 5px;
            font-family: sans-serif;
        }
        .footer b {
            color: #4CAF50;
        }
    </style>
    <div class="footer">
        <b>Pró-Corpo BI</b> | 🤖
    </div>
    """, unsafe_allow_html=True)

# Upload dos arquivos
st.subheader("📤 Upload dos Arquivos")

col1, col2 = st.columns(2)
with col1:
    appointments_sheet = st.file_uploader(
        "**Base de Agendamentos** (Excel/CSV)", 
        type=["xlsx", "xls", "csv"],
        help="Faça upload da planilha com os dados de agendamentos"
    )

with col2:
    indicate_excel = st.file_uploader(
        "**Base do Indique & Multiplique** (Excel/CSV)", 
        type=["xlsx", "xls", "csv"],
        help="Faça upload da planilha com os dados da campanha"
    )

# Processamento dos dados
if st.button("🔍 Processar Dados", help="Clique para processar os dados"):
    if appointments_sheet is not None and indicate_excel is not None:
        with st.spinner("Processando dados... Por favor, aguarde."):
            try:
                # appointments_df = treating_appointments(appointments_sheet)
                indique_df = treating_indicate(indicate_excel)
                # df_final = merge_and_groupby(indique_df, appointments_df)
                
                st.session_state['indique_df'] = indique_df
                st.success("✅ Dados processados com sucesso!")
                
            except Exception as e:
                st.error(f"❌ Ocorreu um erro ao processar os dados: {str(e)}")
    else:
        st.warning("⚠️ Por favor, faça upload de ambos os arquivos antes de processar.")

# Exibição dos resultados
if 'indique_df' in st.session_state:
    st.markdown("---")
    st.subheader("📋 Resultados Consolidados")
    
    # Mostrar dataframe com estilo
    st.dataframe(
        st.session_state['indique_df'].style
        .background_gradient(cmap='Blues')
        .set_properties(**{'text-align': 'left'})
        .format(precision=2),
        use_container_width=True
    )
    
    # Botão de download
    st.markdown("---")
    st.subheader("📥 Exportar Resultados")
    
    def to_excel(df):
        try:
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Resultados')
            return output.getvalue()
        except Exception as e:
            st.error(f"Erro ao gerar arquivo Excel: {str(e)}")
            return None
    
    excel_data = to_excel(st.session_state['indique_df'])
    
    if excel_data is not None:
        st.download_button(
            label="⬇️ Baixar Planilha em Excel",
            data=excel_data,
            file_name="Resultados_Indique_Multiplique.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            help="Clique para baixar os resultados em formato Excel"
        )    
# Rodapé
st.markdown("---")
st.markdown('<div class="footer">Pró-Corpo BI | 🤖</div>', unsafe_allow_html=True)