import streamlit as st
from email_notifications import correo_producto_publicado

st.title("📦 Publicar Producto")

nombre_producto = st.text_input("Nombre del Producto")
precio = st.number_input("Precio", min_value=0.1)

if st.button("Publicar Producto"):
    usuario_email = st.session_state.get("user_email", "")
    if usuario_email:
        # 📧 Enviar notificación de producto agregado
        correo_producto_publicado(usuario_email, nombre_producto)
        st.success("Producto publicado con éxito. Revisa tu correo.")
    else:
        st.error("Debes iniciar sesión para publicar productos.")
