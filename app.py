import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Cargar los archivos Excel
df_preguntas = pd.read_excel("preguntas.xlsx")
df_recomendaciones = pd.read_excel("recomendaciones_COBIT2019.xlsx")

st.set_page_config(page_title="Auditoría COBIT 2019", layout="wide")
st.title("🛡️ Evaluación de Auditoría de Sistemas - COBIT 2019")

st.write("Por favor responde las siguientes preguntas seleccionando un nivel del 1 al 5:")

respuestas_usuario = {}

# Mostrar las preguntas con sliders
for i, row in df_preguntas.iterrows():
    clave = f"{row['Dominio']} - {row['Pregunta']}"
    respuesta = st.slider(f"**{row['Pregunta']}**", 1, 5, 3, key=clave)
    respuestas_usuario[clave] = respuesta

# Botón para procesar resultados
if st.button("📊 Generar informe"):
    st.subheader("🔍 Resultados del cuestionario")
    
    # Crear dataframe con respuestas
    df_respuestas = df_preguntas.copy()
    df_respuestas["Respuesta"] = [
        respuestas_usuario[f"{row['Dominio']} - {row['Pregunta']}"]
        for i, row in df_preguntas.iterrows()
    ]
    
    # Calcular promedios por dominio
    promedios = df_respuestas.groupby("Dominio")["Respuesta"].mean().reset_index()
    
    # Mostrar radar chart
    st.markdown("### 🕸️ Promedio por dominio (Radar Chart)")
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=promedios["Respuesta"],
        theta=promedios["Dominio"],
        fill='toself',
        name='Promedio'
    ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    # Mostrar semáforos por dominio
    st.markdown("### 🚦 Indicadores por dominio")
    for index, row in promedios.iterrows():
        color = "🟥 Rojo" if row["Respuesta"] < 2.5 else "🟨 Amarillo" if row["Respuesta"] < 4 else "🟩 Verde"
        st.write(f"**{row['Dominio']}**: Promedio = {row['Respuesta']:.2f} → {color}")

    # Interpretación general
    st.markdown("### 📘 Interpretación general")
    p
