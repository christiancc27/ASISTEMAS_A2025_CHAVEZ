import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Auditoría COBIT 2019", layout="centered")
st.title("🛡️ Evaluación de Auditoría – COBIT 2019")

# Subida del archivo Excel
uploaded_file = st.file_uploader("📤 Sube el archivo Excel con preguntas y recomendaciones", type=["xlsx"])

if uploaded_file:
    df_raw = pd.read_excel(uploaded_file)

    # Nos quedamos con preguntas únicas para mostrar (sin repetir por cada valor)
    df_preguntas = df_raw.drop_duplicates(subset=["Dominio", "Pregunta"]).reset_index(drop=True)

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

        # Convertimos respuestas a DataFrame
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

        # Interpretación semaforizada
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
            st.info(f"Recomendación: {row['Recomendación']}")
