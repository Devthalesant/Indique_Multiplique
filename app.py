import streamlit as st
from Functions.treating_bases import *

st.title("Campanha Indique & Multiplique")


appointments_sheet = st.file_uploader("Anexe a Base de Agendamentos:")
indicate_excel = st.file_uploader("Anexe a Base do Indique & Multiplique:")



appointments_df = treating_appointments(appointments_sheet)

indique_df = treating_indicate(indicate_excel)

df_final = merge_and_groupby(indique_df,appointments_df)

st.dataframe(df_final)