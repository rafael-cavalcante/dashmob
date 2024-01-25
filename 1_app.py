import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="DashMob",
    page_icon="📊",
    layout="wide")

df = pd.read_csv("acidentes2023_todas_causas_tipos.csv", delimiter=";", encoding="ISO-8859-1")

st.title("📊 DashMob Acidentes Rodoviarios PRF - 2023")

st.header("Painel sobre Mobilidade `version 1`")

#Gráfico 01
df_tipo_acidente = df['tipo_acidente'].value_counts().reset_index(name="total")

fig_tipos_acidente = px.bar(df_tipo_acidente, x="tipo_acidente", y="total", color="total", title="Quantidade de Acidentes por Tipo")
fig_tipos_acidente.update_layout(xaxis_title= "Tipo de Acidente", yaxis_title= "Quantidade")

st.plotly_chart(fig_tipos_acidente, use_container_width=True)

df_estados = df["uf"].unique()

list_estados = list(df_estados)

list_estados.insert(0, "TODOS")

estado = st.selectbox("Estado", list_estados)

if(estado == "TODOS"):
    df_municipios = df
else:
    df_municipios = df[df["uf"] == estado]