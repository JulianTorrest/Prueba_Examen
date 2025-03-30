import streamlit as st
import pandas as pd
import os
from email_notifications import (
    correo_registro,
    correo_producto_publicado,
    correo_confirmacion_compra,
    correo_notificacion_vendedor
)

# Configuración de la aplicación
st.set_page_config(page_title="📦 Marketplace", layout="wide")

# Archivo de almacenamiento de productos
DATA_FILE = "productos.csv"

# Cargar productos desde el archivo CSV
def cargar_productos():
    if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
        try:
            return pd.read_csv(DATA_FILE)
        except pd.errors.EmptyDataError:
            return pd.DataFrame(columns=["nombre", "precio", "vendedor", "imagen"])
    return pd.DataFrame(columns=["nombre", "precio", "vendedor", "imagen"])

# Guardar un nuevo producto en el CSV
def guardar_producto(nombre, precio, vendedor, imagen):
    df = cargar_productos()
    nuevo_producto = pd.DataFrame([[nombre, precio, vendedor, imagen]], columns=df.columns)
    df = pd.concat([df, nuevo_producto], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

# Manejo de sesión del usuario
if "user_email" not in st.session_state:
    st.session_state["user_email"] = None
    st.session_state["user_name"] = None

def cerrar_sesion():
    st.session_state["user_email"] = None
    st.session_state["user_name"] = None
    st.experimental_rerun()

# Sección de autenticación en la barra lateral
st.sidebar.title("👤 Usuario")
if st.session_state["user_email"]:
    st.sidebar.success(f"Sesión iniciada como {st.session_state['user_name']}")
    if st.sidebar.button("Cerrar sesión"):
        cerrar_sesion()
else:
    with st.sidebar.form("login_form"):
        nombre = st.text_input("Nombre")
        email = st.text_input("Correo electrónico")
        submitted = st.form_submit_button("Registrarse / Iniciar sesión")
        
        if submitted:
            if nombre and email:
                st.session_state["user_email"] = email
                st.session_state["user_name"] = nombre
                correo_registro(email, nombre)
                st.sidebar.success("Registro exitoso. Revisa tu correo.")
                st.experimental_rerun()
            else:
                st.sidebar.error("⚠️ Completa todos los campos.")

# Página principal: Marketplace
st.title("📦 Marketplace de Productos")
productos = cargar_productos()

if not productos.empty:
    for _, producto in productos.iterrows():
        with st.container():
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(producto["imagen"], width=150)
            with col2:
                st.subheader(producto["nombre"])
                st.write(f"💰 Precio: ${producto['precio']}")
                st.write(f"📧 Vendedor: {producto['vendedor']}")
                
                if st.button(f"🛒 Comprar {producto['nombre']}", key=producto["nombre"]):
                    if st.session_state["user_email"]:
                        correo_confirmacion_compra(st.session_state["user_email"], producto["nombre"], producto["precio"])
                        correo_notificacion_vendedor(producto["vendedor"], st.session_state["user_email"], producto["nombre"])
                        st.success("Compra realizada. Revisa tu correo.")
                    else:
                        st.error("⚠️ Debes iniciar sesión para comprar.")

# Sección para agregar nuevos productos
def agregar_producto():
    st.sidebar.title("➕ Agregar Producto")
    with st.sidebar.form("add_product_form"):
        nombre_producto = st.text_input("Nombre del Producto")
        precio_producto = st.number_input("Precio", min_value=0.1)
        imagen_url = st.text_input("URL de la Imagen")
        submitted = st.form_submit_button("Publicar Producto")
        
        if submitted:
            if st.session_state["user_email"]:
                if nombre_producto and precio_producto and imagen_url:
                    guardar_producto(nombre_producto, precio_producto, st.session_state["user_email"], imagen_url)
                    correo_producto_publicado(st.session_state["user_email"], nombre_producto)
                    st.sidebar.success("Producto agregado con éxito. Revisa tu correo.")
                    st.experimental_rerun()
                else:
                    st.sidebar.error("⚠️ Completa todos los campos.")
            else:
                st.sidebar.error("⚠️ Debes iniciar sesión para agregar productos.")

# Ejecutar la función para agregar productos
agregar_producto()
