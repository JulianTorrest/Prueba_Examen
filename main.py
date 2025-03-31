import streamlit as st
import pandas as pd
import os
import requests
import base64
import hashlib
import streamlit as st

# Configuración de la aplicación
st.set_page_config(page_title="📦 Marketplace", layout="centered")

# Configuración de GitHub
GITHUB_REPO = "Prueba_Examen"
GITHUB_FILE_PATH = "productos.csv"
GITHUB_USERNAME = "JulianTorrest"
GITHUB_TOKEN = "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"
GITHUB_RAW_URL = f"https://raw.githubusercontent.com/JulianTorrest/Prueba_Examen/main/productos.csv"
API_URL = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

# Archivo de tasas de cambio
TASA_CAMBIO_FILE = f"https://raw.githubusercontent.com/JulianTorrest/Prueba_Examen/main/tasa_cambio.csv"
# Configuración inicial de sesión
if "user_email" not in st.session_state:
    st.session_state["user_email"] = None
    st.session_state["user_name"] = None

# Función para cifrar contraseñas con SHA256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Función para cargar usuarios registrados
def cargar_usuarios():
    try:
        return pd.read_csv(USUARIOS_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Nombre", "Email", "Contraseña"])
    except Exception as e:
        st.error(f"⚠️ Error al leer usuarios: {e}")
        return pd.DataFrame()

# Función para registrar un usuario
def registrar_usuario(nombre, email, password):
    usuarios = cargar_usuarios()
    if email in usuarios["Email"].values:
        st.warning("⚠️ Este correo ya está registrado. Inicia sesión.")
        return False
    else:
        hashed_password = hash_password(password)
        nuevo_usuario = pd.DataFrame([[nombre, email, hashed_password]], columns=["Nombre", "Email", "Contraseña"])
        usuarios = pd.concat([usuarios, nuevo_usuario], ignore_index=True)
        usuarios.to_csv(USUARIOS_FILE, index=False)
        st.success("✅ Registro exitoso. Ahora puedes iniciar sesión.")
        return True

# Función para iniciar sesión
def iniciar_sesion(email, password):
    usuarios = cargar_usuarios()
    if email in usuarios["Email"].values:
        user_data = usuarios.loc[usuarios["Email"] == email]
        stored_password = user_data["Contraseña"].values[0]
        
        if stored_password == hash_password(password):
            st.session_state["user_email"] = email
            st.session_state["user_name"] = user_data["Nombre"].values[0]
            st.sidebar.success(f"🔓 Sesión iniciada como {st.session_state['user_name']}")
            st.experimental_rerun()
        else:
            st.error("⚠️ Contraseña incorrecta.")
    else:
        st.error("⚠️ Correo no registrado. Regístrate primero.")

# Función para cerrar sesión
def cerrar_sesion():
    st.session_state["user_email"] = None
    st.session_state["user_name"] = None
    st.experimental_rerun()

# 📌 Sección de usuario en la barra lateral
st.sidebar.title("👤 Usuario")

if st.session_state["user_email"]:
    st.sidebar.success(f"🔓 Sesión iniciada como {st.session_state['user_name']}")
    if st.sidebar.button("Cerrar sesión"):
        cerrar_sesion()
else:
    # Sección de registro
    st.sidebar.subheader("🆕 Registrarse")
    with st.sidebar.form("registro_form"):
        nombre_registro = st.text_input("Nombre Completo")
        email_registro = st.text_input("Correo Electrónico")
        password_registro = st.text_input("Contraseña", type="password")
        submitted_registro = st.form_submit_button("Registrarse")
        
        if submitted_registro and nombre_registro and email_registro and password_registro:
            registrar_usuario(nombre_registro, email_registro, password_registro)

    # Sección de inicio de sesión
    st.sidebar.subheader("🔑 Iniciar Sesión")
    with st.sidebar.form("login_form"):
        email_login = st.text_input("Correo Electrónico", key="email_login")
        password_login = st.text_input("Contraseña", type="password", key="password_login")
        submitted_login = st.form_submit_button("Iniciar sesión")
        
        if submitted_login and email_login and password_login:
            iniciar_sesion(email_login, password_login)

# 📦 Marketplace de Productos
st.title("📦 Marketplace de Productos")

# Función para cargar productos
def cargar_productos():
    try:
        return pd.read_csv(PRODUCTOS_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["nombre", "descripcion", "precio_local", "precio_internacional", "moneda", "vendedor", "imagen"])
    except Exception as e:
        st.error(f"⚠️ Error al leer productos: {e}")
        return pd.DataFrame()

# Función para cargar tasas de cambio
def cargar_tasas_cambio():
    try:
        return pd.read_csv(TASA_CAMBIO_FILE, index_col="moneda").to_dict()["tasa"]
    except FileNotFoundError:
        return {}
    except Exception as e:
        st.error(f"⚠️ Error al leer tasas de cambio: {e}")
        return {}

# Función para guardar producto
def guardar_producto(nombre, descripcion, precio_local, moneda, vendedor, imagen):
    df = cargar_productos()
    tasas_cambio = cargar_tasas_cambio()

    if moneda in tasas_cambio:
        precio_internacional = round(precio_local * tasas_cambio[moneda], 2)
    else:
        precio_internacional = "No disponible"

    nuevo_producto = pd.DataFrame([[nombre, descripcion, precio_local, precio_internacional, moneda, vendedor, imagen]], 
                                  columns=df.columns)
    df = pd.concat([df, nuevo_producto], ignore_index=True)
    df.to_csv(PRODUCTOS_FILE, index=False)
    st.success("✅ Producto guardado correctamente.")

# Mostrar productos disponibles
productos = cargar_productos()

if not productos.empty:
    for _, producto in productos.iterrows():
        with st.container():
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(producto["imagen"], width=150)
            with col2:
                st.subheader(producto["nombre"])
                st.write(f"📝 {producto['descripcion']}")
                st.write(f"💰 Precio Local: {producto['precio_local']} {producto['moneda']}")
                st.write(f"🌍 Precio Internacional: {producto['precio_internacional']} USD")
                st.write(f"📧 Vendedor: {producto['vendedor']}")

# 📌 Agregar Nuevo Producto
st.sidebar.title("➕ Agregar Producto")
monedas_disponibles = ["USD", "EUR", "GBP", "RUB", "CAD", "AUD", "NZD"]

with st.sidebar.form("add_product_form"):
    nombre_producto = st.text_input("Nombre del Producto")
    descripcion_producto = st.text_area("Descripción")
    precio_producto = st.number_input("Precio", min_value=0.1)
    moneda_seleccionada = st.selectbox("Moneda", monedas_disponibles)
    imagen_url = st.text_input("URL de la Imagen")
    submitted = st.form_submit_button("Publicar Producto")

    if submitted:
        if st.session_state["user_email"]:
            if nombre_producto and descripcion_producto and precio_producto and moneda_seleccionada and imagen_url:
                guardar_producto(nombre_producto, descripcion_producto, precio_producto, moneda_seleccionada, st.session_state["user_email"], imagen_url)
                st.experimental_rerun()
            else:
                st.sidebar.error("⚠️ Completa todos los campos.")
        else:
            st.sidebar.error("⚠️ Debes iniciar sesión para agregar productos.")
