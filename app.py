import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Auditoría COBIT 2019", layout="centered")

st.title("Aplicación de Auditoría de Sistemas - COBIT 2019")

# Leer archivo Excel local (debe estar en la misma carpeta que app.py)
try:
    df = pd.read_excel("preguntas.xlsx")
except FileNotFoundError:
    st.error("Archivo preguntas.xlsx no encontrado. Por favor verifica que esté en la carpeta del proyecto.")
    st.stop()

# Mostrar las preguntas con sliders
respuestas = []
st.header("Cuestionario")

for idx, row in df.iterrows():
    valor = st.slider(
        f"{row['Dominio']} - {row['Pregunta']}",
        min_value=1,
        max_value=5,
        value=3,
        step=1,
        key=idx
    )
    respuestas.append({
        "Dominio": row["Dominio"],
        "Pregunta": row["Pregunta"],
        "Respuesta": valor,
        "Recomendación": row.get("Recomendación", "")  # Opcional mostrar o usar más adelante
    })

# Botón para generar el informe
if st.button("Generar Informe"):

    df_resp = pd.DataFrame(respuestas)

    # Calcular promedio por dominio
    resumen = df_resp.groupby("Dominio")["Respuesta"].mean().reset_index()

    st.subheader("Resumen de puntuación por dominio")
    st.dataframe(resumen)

    # Gráfico radar
    fig = px.line_polar(
        resumen,
        r='Respuesta',
        theta='Dominio',
        line_close=True,
        range_r=[1, 5],
        title="Promedio de puntuación por dominio"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Mostrar indicadores semáforo + interpretación
    st.subheader("Interpretación de resultados")
    for _, row in resumen.iterrows():
        score = row["Respuesta"]
        dominio = row["Dominio"]

        if score <= 2.0:
            st.error(f"{dominio}: Riesgo Alto ({score:.2f}) — Se requiere intervención inmediata.")
        elif score <= 3.5:
            st.warning(f"{dominio}: Riesgo Medio ({score:.2f}) — Oportunidad de mejora.")
        else:
            st.success(f"{dominio}: Cumplimiento Bueno ({score:.2f}) — Controles adecuados.")

    # Opcional: mostrar recomendaciones según respuesta promedio
    st.subheader("Recomendaciones generales por dominio")
    for dominio in resumen["Dominio"]:
        # Puedes agregar lógica para mostrar recomendaciones basadas en promedios o individuales
        st.write(f"Dominio {dominio}:")
        # Aquí podrías filtrar df o df_resp para recomendaciones específicas
        # Por simplicidad, solo mostramos un placeholder:
        st.write("Revisar recomendaciones específicas en el cuestionario.")