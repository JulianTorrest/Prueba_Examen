import streamlit as st
import pandas as pd
import os
from email_notifications import correo_confirmacion_compra, correo_notificacion_vendedor

# Ruta del archivo CSV en el mismo proyecto
PRODUCTOS_CSV = "productos.csv"

def cargar_productos():
    """Carga los productos desde el archivo CSV."""
    if os.path.exists(PRODUCTOS_CSV):
        return pd.read_csv(PRODUCTOS_CSV).to_dict(orient="records")
    return []

def guardar_producto(nombre, precio, vendedor):
    """Guarda un nuevo producto en el archivo CSV."""
    productos = cargar_productos()
    productos.append({"nombre": nombre, "precio": precio, "vendedor": vendedor})
    pd.DataFrame(productos).to_csv(PRODUCTOS_CSV, index=False)

# Cargar productos disponibles
productos = cargar_productos()

st.title("🛍️ Comprar Producto")

# Verificar si el usuario ha iniciado sesión
if "user_email" not in st.session_state:
    st.warning("⚠️ Debes iniciar sesión para ver y comprar productos.")
else:
    comprador_email = st.session_state["user_email"]

    if not productos:
        st.info("No hay productos disponibles en este momento.")
    else:
        for producto in productos:
            with st.container():
                st.subheader(producto["nombre"])
                st.write(f"💰 **Precio:** ${producto['precio']}")
                st.write(f"👤 **Vendedor:** {producto['vendedor']}")

                if st.button(f"🛒 Comprar {producto['nombre']}", key=producto["nombre"]):
                    if comprador_email:
                        # 📧 Notificación al comprador
                        correo_confirmacion_compra(comprador_email, producto["nombre"], producto["precio"])

                        # 📧 Notificación al vendedor
                        correo_notificacion_vendedor(producto["vendedor"], comprador_email, producto["nombre"])

                        st.success(f"✅ Compra realizada. Revisa tu correo ({comprador_email}).")
                    else:
                        st.error("Debes iniciar sesión para comprar.")
