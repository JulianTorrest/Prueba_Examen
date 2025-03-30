import streamlit as st
import pandas as pd
from payments import guardar_producto

st.title("📦 Subir un nuevo producto")

if "user_email" not in st.session_state:
    st.warning("⚠️ Debes iniciar sesión para subir productos.")
else:
    nombre_producto = st.text_input("Nombre del Producto")
    precio = st.number_input("Precio", min_value=1)
    vendedor = st.session_state["user_email"]

    if st.button("Subir Producto"):
        if nombre_producto and precio:
            guardar_producto(nombre_producto, precio, vendedor)
            st.success("✅ Producto agregado exitosamente.")
        else:
            st.error("Por favor, completa todos los campos.")
