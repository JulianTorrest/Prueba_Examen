import streamlit as st
import pandas as pd
import requests
import os
import base64
import json
from email_notifications import correo_registro

# Configuración de GitHub
GITHUB_REPO = "Prueba_Examen"
GITHUB_FILE_PATH = "usuarios.csv"
GITHUB_USERNAME = "JulianTorrest"
GITHUB_TOKEN = "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"  # 🔑 Reemplaza con tu token de GitHub
GITHUB_RAW_URL = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{GITHUB_REPO}/main/{GITHUB_FILE_PATH}"
API_URL = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

# Cargar usuarios desde GitHub
def cargar_usuarios():
    """Descarga el archivo CSV de usuarios desde GitHub y lo convierte en DataFrame."""
    try:
        response = requests.get(GITHUB_RAW_URL)
        response.raise_for_status()  # Lanza un error si falla la solicitud
        return pd.read_csv(pd.compat.StringIO(response.text))
    except Exception:
        return pd.DataFrame(columns=["nombre", "email"])  # Si hay error, devuelve DataFrame vacío

# Guardar un nuevo usuario en GitHub
def guardar_usuario(nombre, email):
    """Agrega un usuario al CSV y lo actualiza en GitHub."""
    try:
        df = cargar_usuarios()
        
        # Verificar si el usuario ya existe
        if email in df["email"].values:
            return False  # Usuario ya registrado
        
        # Agregar nuevo usuario
        nuevo_usuario = pd.DataFrame([[nombre, email]], columns=df.columns)
        df = pd.concat([df, nuevo_usuario], ignore_index=True)

        # Convertir DataFrame a CSV
        nuevo_contenido = df.to_csv(index=False)

        # Codificar en base64 para subir a GitHub
        contenido_base64 = base64.b64encode(nuevo_contenido.encode()).decode()

        # Obtener SHA del archivo existente en GitHub
        response = requests.get(API_URL, headers=HEADERS)
        sha = response.json().get("sha", "")

        # Crear payload para GitHub
        data = {
            "message": "🆕 Registro de usuario",
            "content": contenido_base64,
            "sha": sha,
            "branch": "main"
        }

        # Subir archivo actualizado a GitHub
        response = requests.put(API_URL, headers=HEADERS, data=json.dumps(data))

        return response.status_code in [200, 201]  # Devuelve True si la actualización fue exitosa

    except Exception as e:
        st.error(f"⚠️ Error al guardar usuario: {e}")
        return False

# Verificar si un usuario está registrado
def usuario_existe(email):
    df = cargar_usuarios()
    return email in df["email"].values

# Configurar sesión de usuario
if "user" not in st.session_state:
    st.session_state["user"] = None
    st.session_state["user_email"] = None

# Título de la app
st.title("🔑 Autenticación")

# Opciones de autenticación
modo = st.radio("Selecciona una opción", ["Registrarse", "Iniciar sesión"])

# Registro de usuario
if modo == "Registrarse":
    st.subheader("📝 Registro de Usuario")
    nombre = st.text_input("Nombre")
    email = st.text_input("Correo electrónico")

    if st.button("Registrarse"):
        if nombre and email:
            if usuario_existe(email):
                st.warning("❌ Este correo ya está registrado. Intenta iniciar sesión.")
            else:
                if guardar_usuario(nombre, email):
                    correo_registro(email, nombre)  # Enviar correo de bienvenida
                    st.success("✅ Registro exitoso. Revisa tu correo.")
                else:
                    st.error("❌ Error al registrar usuario.")
        else:
            st.error("⚠️ Completa todos los campos.")

# Inicio de sesión
if modo == "Iniciar sesión":
    st.subheader("🔓 Iniciar Sesión")
    email_login = st.text_input("Correo electrónico")

    if st.button("Ingresar"):
        if usuario_existe(email_login):
            df = cargar_usuarios()
            st.session_state["user_email"] = email_login
            st.session_state["user"] = df.query(f'email == "{email_login}"')["nombre"].values[0]
            st.success(f"✅ Bienvenido {st.session_state['user']}")
        else:
            st.error("❌ Usuario no registrado. Intenta registrarte.")

# Cierre de sesión
if st.session_state["user"]:
    if st.button("Cerrar sesión"):
        st.session_state["user"] = None
        st.session_state["user_email"] = None
        st.success("🔒 Sesión cerrada. Hasta pronto.")
        st.experimental_rerun()
