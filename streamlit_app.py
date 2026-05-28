import streamlit as st
import requests


st.set_page_config(
    page_title="AI Operational Middleware",
    layout="centered",
)

st.title("AI Operational Middleware")

brand_id = st.selectbox(
    "Selecciona marca",
    options=[1],
)

product_name = st.text_input(
    "Nombre producto",
    placeholder="Ej: Monstera Deliciosa",
)

product_details = st.text_area(
    "Detalles",
    placeholder="Ej: Planta tropical de hojas grandes decorativas",
)

if st.button("Generar contenido"):

    payload = {
        "brand_id": brand_id,
        "name": product_name,
        "details": product_details,
    }

    with st.spinner("Generando contenido..."):

        response = requests.post(
            "http://127.0.0.1:8000/generate",
            json=payload,
        )

    if response.status_code == 200:

        data = response.json()

        st.success("Contenido generado")

        st.subheader("Caption")
        st.write(data["caption"])

        st.subheader("Hashtags")
        st.write(" ".join(data["hashtags"]))

        st.subheader("CTA")
        st.write(data["cta"])

    else:
        st.error("Error generando contenido")