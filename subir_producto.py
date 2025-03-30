import streamlit as st
import pandas as pd
import requests
import base64
import json

# Configuración de GitHub
GITHUB_REPO = "Prueba_Examen"  # Reemplaza con tu repositorio
GITHUB_FILE_PATH = "productos.csv"
GITHUB_USERNAME = "JulianTorrest"  # Tu usuario de GitHub
GITHUB_TOKEN = "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"  # 🔑 Usa un token con permisos de escritura
GITHUB_RAW_URL = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{GITHUB_REPO}/main/{GITHUB_FILE_PATH}"

# URL API de GitHub para obtener y actualizar el archivo
API_URL = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

def obtener_contenido_csv():
    """Descarga el contenido actual del archivo CSV desde GitHub."""
    try:
        response = requests.get(GITHUB_RAW_URL)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException:
        return "nombre,precio,vendedor\n"  # Inicializa si no existe el archivo

def actualizar_csv(nuevo_producto):
    """Actualiza el archivo CSV con un nuevo producto y lo sube a GitHub."""
    try:
        # Obtener contenido actual
        contenido_actual = obtener_contenido_csv()

        # Agregar el nuevo producto
        nuevo_contenido = contenido_actual + f"{nuevo_producto['nombre']},{nuevo_producto['precio']},{nuevo_producto['vendedor']}\n"

        # Codificar en base64
        contenido_base64 = base64.b64encode(nuevo_contenido.encode()).decode()

        # Obtener SHA del archivo
        response = requests.get(API_URL, headers=HEADERS)
        sha = response.json().get("sha", "")

        # Realizar commit con la actualización
        data = {
            "message": "🆕 Producto agregado automáticamente",
            "content": contenido_base64,
            "sha": sha,
            "branch": "main"
        }
        response = requests.put(API_URL, headers=HEADERS, data=json.dumps(data))

        if response.status_code in [200, 201]:
            st.success("✅ Producto agregado exitosamente y subido a GitHub.")
        else:
            st.error(f"❌ Error al subir a GitHub: {response.text}")

    except Exception as e:
        st.error(f"⚠️ Ocurrió un error: {e}")

# 📌 Interfaz en Streamlit para agregar productos
st.title("📦 Agregar Nuevo Producto")

with st.form("form_agregar_producto"):
    nombre = st.text_input("Nombre del producto")
    precio = st.number_input("Precio", min_value=0.01, format="%.2f")
    vendedor = st.text_input("Correo del vendedor")

    submit = st.form_submit_button("➕ Agregar Producto")

if submit:
    if nombre and precio and vendedor:
        nuevo_producto = {"nombre": nombre, "precio": precio, "vendedor": vendedor}
        actualizar_csv(nuevo_producto)
    else:
        st.warning("⚠️ Todos los campos son obligatorios.")

