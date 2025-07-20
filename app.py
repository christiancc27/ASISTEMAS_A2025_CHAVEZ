import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Auditoría COBIT 2019", layout="centered")
st.title("🛡️ Evaluación de Auditoría – COBIT 2019")

# Cargar los archivos directamente desde el directorio del proyecto
try:
    df_raw = pd.read_excel("recomendaciones_COBIT2019.xlsx")
    df_preguntas = pd.read_excel("preguntas.xlsx")
except FileNotFoundError:
    st.error("❌ No se encontraron los archivos 'preguntas.xlsx' y/o 'recomendaciones_COBIT2019.xlsx'. "
             "Por favor asegúrate de que estén en la misma carpeta que este archivo.")
    st.stop()

# Preguntas únicas para mostrar
df_preguntas = df_preguntas.drop_duplicates(subset=["Dominio", "Pregunta"]).reset_index(drop=True)

st.subheader("📝 Cuestionario")
respuestas = []

# Mostrar preguntas
for idx, row in df_preguntas.iterrows():
    valor = st.slider(
        f"{row['Dominio']} – {row['Pregunta']}",
        min_value=1, max_value=5, value=3, step=1
    )
    respuestas.append({
        "Dominio": row["Dominio"],
        "Pregunta": row["Pregunta"],
        "Respuesta": valor
    })

# Botón para procesar
if st.button("✅ Generar Informe"):
    st.subheader("📊 Resultados por Dominio")

    # Convertir respuestas en DataFrame
    df_resp = pd.DataFrame(respuestas)

    # Cálculo de promedios por dominio
    resumen = df_resp.groupby("Dominio")["Respuesta"].mean().reset_index()

    # Mostrar tabla resumen
    st.dataframe(resumen)

    # Gráfico radar
    fig = px.line_polar(
        resumen,
        r='Respuesta',
        theta='Dominio',
        line_close=True,
        range_r=[0, 5],
        title="Gráfico de Radar – Evaluación por Dominio"
    )
    st.plotly_chart(fig)

    # Interpretación tipo semáforo
    st.subheader("🟢 Interpretación por Dominio")
    for _, row in resumen.iterrows():
        if row["Respuesta"] < 2.1:
            st.error(f"{row['Dominio']}: Riesgo Alto ({row['Respuesta']:.2f}) – Se requiere intervención inmediata.")
        elif row["Respuesta"] < 3.6:
            st.warning(f"{row['Dominio']}: Riesgo Medio ({row['Respuesta']:.2f}) – Existen oportunidades de mejora.")
        else:
            st.success(f"{row['Dominio']}: Cumplimiento Bueno ({row['Respuesta']:.2f}) – Controles adecuados.")

    # Recomendaciones detalladas
    st.subheader("💡 Recomendaciones por Pregunta")
    df_merged = pd.merge(df_resp, df_raw, on=["Dominio", "Pregunta", "Respuesta"], how="left")

    for idx, row in df_merged.iterrows():
        st.markdown(f"**{idx+1}. {row['Pregunta']}**")
        if pd.notna(row["Recomendación"]):
            st.info(f"Recomendación: {row['Recomendación']}")
        else:
            st.warning("No se encontró una recomendación para esta respuesta.")
