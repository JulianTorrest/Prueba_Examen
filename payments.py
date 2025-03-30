import streamlit as st
from email_notifications import correo_confirmacion_compra, correo_notificacion_vendedor

st.title("🛍️ Comprar Producto")

productos = [
    {"nombre": "Laptop", "precio": 500, "vendedor": "vendedor@email.com"},
    {"nombre": "Teléfono", "precio": 300, "vendedor": "otro@email.com"},
]

for producto in productos:
    st.subheader(producto["nombre"])
    st.write(f"💰 Precio: ${producto['precio']}")
    if st.button(f"Comprar {producto['nombre']}"):
        comprador_email = st.session_state.get("user_email", "")
        if comprador_email:
            # 📧 Notificación al comprador
            correo_confirmacion_compra(comprador_email, producto["nombre"], producto["precio"])

            # 📧 Notificación al vendedor
            correo_notificacion_vendedor(producto["vendedor"], comprador_email, producto["nombre"])

            st.success("Compra realizada. Revisa tu correo.")
        else:
            st.error("Debes iniciar sesión para comprar.")
