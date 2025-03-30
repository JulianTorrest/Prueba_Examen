import streamlit as st
import pandas as pd
import os
from email_notifications import correo_registro

# Archivo donde se almacenan los usuarios (simulación de base de datos)
USERS_FILE = "usuarios.csv"

# Cargar usuarios desde archivo CSV
def cargar_usuarios():
    if os.path.exists(USERS_FILE):
        return pd.read_csv(USERS_FILE)
    return pd.DataFrame(columns=["nombre", "email"])

# Guardar un nuevo usuario
def guardar_usuario(nombre, email):
    df = cargar_usuarios()
    if email in df["email"].values:
        return False  # El usuario ya existe
    nuevo_usuario = pd.DataFrame([[nombre, email]], columns=df.columns)
    df = pd.concat([df, nuevo_usuario], ignore_index=True)
    df.to_csv(USERS_FILE, index=False)
    return True

# Verificar si un usuario está registrado
def usuario_existe(email):
    df = cargar_usuarios()
    return email in df["email"].values

# Configurar la sesión
if "user" not in st.session_state:
    st.session_state["user"] = None
    st.session_state["user_email"] = None

# Título de la página
st.title("🔑 Autenticación")

# Opciones de autenticación
modo = st.radio("Selecciona una opción", ["Registrarse", "Iniciar sesión"])

# Sección de registro
if modo == "Registrarse":
    st.subheader("📝 Registro de Usuario")
    nombre = st.text_input("Nombre")
    email = st.text_input("Correo electrónico")

    if st.button("Registrarse"):
        if nombre and email:
            if usuario_existe(email):
                st.warning("❌ Este correo ya está registrado. Intenta iniciar sesión.")
            else:
                guardar_usuario(nombre, email)
                correo_registro(email, nombre)  # Enviar correo de bienvenida
                st.success("✅ Registro exitoso. Revisa tu correo.")
        else:
            st.error("⚠️ Completa todos los campos.")

# Sección de inicio de sesión
if modo == "Iniciar sesión":
    st.subheader("🔓 Iniciar Sesión")
    email_login = st.text_input("Correo electrónico")

    if st.button("Ingresar"):
        if usuario_existe(email_login):
            st.session_state["user_email"] = email_login
            st.session_state["user"] = cargar_usuarios().query(f'email == "{email_login}"')["nombre"].values[0]
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
