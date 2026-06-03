import requests
import streamlit as st

from src.ice_repository import create_business_profile, get_business_profiles


st.set_page_config(
    page_title="AI Operational Middleware",
    layout="centered",
)

st.title("AI Operational Middleware")

app_mode = st.sidebar.selectbox(
    "Modo",
    options=[
        "AI Middleware Demo",
        "Instagram Content Engine",
    ],
)


if app_mode == "Instagram Content Engine":
    st.header("Instagram Content Engine")
    st.caption("Sprint 0 — T-01 Business Profile")

    st.subheader("Crear perfil de negocio")

    with st.form("business_profile_form"):
        nombre_negocio = st.text_input(
            "Nombre del negocio",
            max_chars=100,
            placeholder="Ej: NOVO",
        )

        rubro = st.text_input(
            "Rubro",
            max_chars=100,
            placeholder="Ej: Café de especialidad",
        )

        ciudad = st.text_input(
            "Ciudad",
            max_chars=100,
            placeholder="Ej: Santiago",
        )

        submitted = st.form_submit_button("Guardar perfil")

    if submitted:
        if not nombre_negocio or not rubro or not ciudad:
            st.error("Completa nombre del negocio, rubro y ciudad.")
        else:
            profile_id = create_business_profile(
                nombre_negocio=nombre_negocio,
                rubro=rubro,
                ciudad=ciudad,
            )

            st.success(f"Perfil creado correctamente. ID: {profile_id}")

    st.divider()

    st.subheader("Perfiles guardados")

    profiles = get_business_profiles()

    if profiles:
        for profile in profiles:
            st.write(
                f"**{profile['nombre_negocio']}** — "
                f"{profile['rubro']} — "
                f"{profile['ciudad']} "
                f"(ID: {profile['id']})"
            )
    else:
        st.info("Aún no hay perfiles guardados.")


else:
    st.header("AI Middleware Demo")

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