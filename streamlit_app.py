import requests
import streamlit as st


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

        runtime_intelligence = data.get(
            "runtime_intelligence",
            {},
        )

        st.divider()

        st.subheader("Runtime Intelligence")

        confidence_score = runtime_intelligence.get(
            "confidence_score",
            0,
        )

        st.metric(
            "Confidence Score",
            f"{confidence_score * 100:.0f}%",
        )

        if runtime_intelligence.get("passed"):
            st.success("QA Passed")
        else:
            st.error("QA Failed")

        issues = runtime_intelligence.get(
            "issues",
            [],
        )

        if issues:
            st.warning("\n".join(issues))
        else:
            st.info("No issues detected")

        with st.expander("Ver runtime intelligence completa"):
            st.json(runtime_intelligence)

    else:
        st.error("Error generando contenido")