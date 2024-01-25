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

ordem_dias_semana = ['segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira', 'sábado', 'domingo']

#Gráfico 01
df_tipo_acidente = df['tipo_acidente'].value_counts().reset_index(name="total")

fig_tipos_acidente = px.bar(df_tipo_acidente, x="tipo_acidente", y="total", color="total", title="Quantidade de Acidentes por Tipo")
fig_tipos_acidente.update_layout(xaxis_title= "Tipo de Acidente", yaxis_title= "Quantidade")

st.plotly_chart(fig_tipos_acidente, use_container_width=True)

col1, col2 = st.columns(2)

#Gráfico 02
df_dia_semana = df["dia_semana"].value_counts().reset_index(name="total")

df_dia_semana['dia_semana'] = pd.Categorical(df_dia_semana['dia_semana'], categories=ordem_dias_semana, ordered=True)

df_dia_semana = df_dia_semana.sort_values(by=["dia_semana"]).reset_index(drop=True)

fig_contagem_por_dias_semana = px.bar(df_dia_semana, x="dia_semana", y="total", color="total")
fig_contagem_por_dias_semana.update_layout(title_text='Contagem de dias da semana', xaxis_title='Dias da semana', yaxis_title='Contagem')

col1.plotly_chart(fig_contagem_por_dias_semana, use_container_width=True)

#Gráfico 03
df_feridos_mortos = df.groupby('dia_semana')[['feridos_leves', 'feridos_graves', 'mortos']].sum().reset_index()

df_feridos_mortos['dia_semana'] = pd.Categorical(df_feridos_mortos['dia_semana'], categories=ordem_dias_semana, ordered=True)

df_feridos_mortos = df_feridos_mortos.sort_values(by=["dia_semana"]).reset_index(drop=True)

df_feridos_mortos = pd.melt(df_feridos_mortos, id_vars='dia_semana', var_name='tipo', value_name='quantidade')

# Criar o gráfico utilizando o Plotly Express
fig_feridos_mortos = px.bar(df_feridos_mortos, x='dia_semana', y='quantidade', color='tipo',
             barmode='group', title='Estatísticas por dia da semana',
             labels={'quantidade': 'Quantidade', 'tipo': 'Tipo'})
fig_feridos_mortos.update_layout(xaxis_title= "Dia da semana", yaxis_title= "Quantidade")

col2.plotly_chart(fig_feridos_mortos, use_container_width=True)

#Gráfico 04
df_uf = df["uf"].value_counts().reset_index(name="total")

fig_por_estado = px.bar(df_uf, x="uf", y="total", color="total", title= "Quantidade de acidentes por estado", labels={'uf': 'Quantidade'})
fig_por_estado.update_layout(xaxis_title= "Estado", yaxis_title= "Quantidade")

st.plotly_chart(fig_por_estado, use_container_width=True)

col3, col4 = st.columns(2)

#Gráfico 05
acidentes_causa_principal = df[df["causa_principal"] == "Sim"]

contagem_acidentes = acidentes_causa_principal['tipo_acidente'].value_counts().reset_index(name="total")

seis_causas_principais = contagem_acidentes.head(6)

fig_causas = px.pie(seis_causas_principais, values="total", names="tipo_acidente", title="Acidentes por causa", color="tipo_acidente")
fig_causas.update_layout(title_text='Gráfico de pizza de acidentes por causa')

col3.plotly_chart(fig_causas, use_container_width=True)

#Gráfico 06
dataset_genero = df["sexo"].value_counts().reset_index(name="total")

fig_genero = px.pie(dataset_genero, values="total", names="sexo", title="Distribuição de acidentes por gênero")

col4.plotly_chart(fig_genero, use_container_width=True)

#Gráfico 07
# Convertendo a coluna "data_inversa" para tipo datetime, se necessário
df["data_inversa"] = pd.to_datetime(df["data_inversa"])

# Extraindo o mês da coluna "data_inversa"
df["mes"] = df["data_inversa"].dt.month

# Obtendo as contagens dos valores únicos nos meses
contagem_total_meses = df["mes"].value_counts().sort_index()

# Mapeando os números dos meses para nomes dos meses
nomes_meses = [
    'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
]
contagem_total_meses.index = [nomes_meses[mes - 1] for mes in contagem_total_meses.index]

# Criando o gráfico de barras com cores diferentes
fig_contagem_total_meses = px.line(contagem_total_meses, x=contagem_total_meses.index, y=contagem_total_meses.values, labels={'x': 'Meses', 'y': 'Contagem'}, title='Contagem total de acidentes por mês')
fig_contagem_total_meses.update_layout(xaxis_title= "Mês", yaxis_title= "Quantidade")

st.plotly_chart(fig_contagem_total_meses, use_container_width=True)

col5, col6 = st.columns(2)

#Gráfico 08
dataset_causa = df["causa_acidente"].value_counts().reset_index(name="total")[0:9]

fig_causa = px.histogram(dataset_causa, x="total", y="causa_acidente", title="Top 10 maiores causas de acidentes")
fig_causa.update_layout(xaxis_title='Número acidentes', yaxis_title='Causas')

col5.plotly_chart(fig_causa, use_container_width=True)

df_estados = df["uf"].unique()

list_estados = list(df_estados)

list_estados.insert(0, "TODOS")

estado = st.selectbox("Estado", list_estados)

if(estado == "TODOS"):
    df_municipios = df
else:
    df_municipios = df[df["uf"] == estado]