import streamlit as st
from email_notifications import enviar_correo

st.title("📦 Marketplace con Notificaciones")

if st.button("Enviar prueba de correo"):
    enviar_correo("usuario@email.com", "¡Hola!", "Este es un email de prueba desde MailerSend.")
    st.success("Correo enviado con éxito.")
