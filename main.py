import streamlit as st
import pandas as pd
import os
import requests
import base64
from email_notifications import (
    correo_registro,
    correo_producto_publicado,
    correo_confirmacion_compra,
    correo_notificacion_vendedor
)

# Configuración de la aplicación
st.set_page_config(page_title="📦 Marketplace", layout="wide")

# Configuración de GitHub
GITHUB_REPO = "Prueba_Examen"
GITHUB_FILE_PATH = "productos.csv"
GITHUB_USERNAME = "JulianTorrest"
GITHUB_TOKEN = "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"
GITHUB_RAW_URL = f"https://raw.githubusercontent.com/JulianTorrest/Prueba_Examen/main/productos.csv"
API_URL = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

# Cargar productos desde GitHub
def cargar_productos():
    try:
        response = requests.get(GITHUB_RAW_URL)
        if response.status_code == 200:
            return pd.read_csv(GITHUB_RAW_URL)
        else:
            st.error(f"⚠️ Error al cargar productos desde GitHub: {response.status_code}")
    except Exception as e:
        st.error(f"⚠️ Error en la carga de productos: {e}")
    return pd.DataFrame(columns=["nombre", "precio", "vendedor", "imagen"])

# Subir productos a GitHub
def guardar_producto(nombre, precio, vendedor, imagen):
    df = cargar_productos()
    nuevo_producto = pd.DataFrame([[nombre, precio, vendedor, imagen]], columns=df.columns)
    df = pd.concat([df, nuevo_producto], ignore_index=True)
    
    csv_data = df.to_csv(index=False)
    try:
        response = requests.get(API_URL, headers=HEADERS)
        if response.status_code == 200:
            file_data = response.json()
            sha = file_data["sha"]
        else:
            sha = None  # Archivo no existe, se creará

        payload = {
            "message": "Actualización de productos",
            "content": base64.b64encode(csv_data.encode()).decode(),
            "branch": "main",
        }
        if sha:
            payload["sha"] = sha

        put_response = requests.put(API_URL, headers=HEADERS, json=payload)
        if put_response.status_code in [200, 201]:
            st.success("✅ Producto guardado correctamente en GitHub.")
        else:
            st.error(f"⚠️ Error al guardar en GitHub: {put_response.status_code}")
    except Exception as e:
        st.error(f"⚠️ Error al subir productos: {e}")

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

