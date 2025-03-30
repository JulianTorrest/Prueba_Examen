import streamlit as st
from email_notifications import correo_registro

st.title("Registro de Usuario")

nombre = st.text_input("Nombre")
email = st.text_input("Correo electrónico")

if st.button("Registrarse"):
    if nombre and email:
        # Guardar usuario en base de datos (ejemplo)
        st.session_state["user"] = nombre
        st.session_state["user_email"] = email
        
        # 📧 Enviar correo de bienvenida
        correo_registro(email, nombre)

        st.success("Registro exitoso. Revisa tu correo.")
    else:
        st.error("Por favor, completa todos los campos.")

