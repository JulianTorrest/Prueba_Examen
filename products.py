import streamlit as st
from email_notifications import correo_producto_publicado

st.title("📦 Publicar Producto")

# Verificar si el usuario ha iniciado sesión
usuario_email = st.session_state.get("user_email", None)
if not usuario_email:
    st.warning("🔒 Debes iniciar sesión para publicar productos.")
    st.stop()

# Formulario de publicación de producto
with st.form("form_publicar_producto"):
    nombre_producto = st.text_input("Nombre del Producto", max_chars=50)
    precio = st.number_input("Precio", min_value=0.1, format="%.2f")
    submit_button = st.form_submit_button("Publicar Producto")

if submit_button:
    if not nombre_producto.strip():
        st.error("⚠️ El nombre del producto no puede estar vacío.")
    else:
        # 📧 Enviar notificación de producto agregado
        correo_producto_publicado(usuario_email, nombre_producto)
        st.success("✅ Producto publicado con éxito. Revisa tu correo.")
        st.experimental_rerun()
