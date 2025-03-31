import streamlit as st
import pandas as pd
import requests
import base64

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

# Función para cargar productos desde GitHub
def cargar_productos():
    try:
        response = requests.get(GITHUB_RAW_URL)
        if response.status_code == 200:
            return pd.read_csv(GITHUB_RAW_URL)
        else:
            st.error(f"⚠️ Error al cargar productos desde GitHub: {response.status_code}")
    except Exception as e:
        st.error(f"⚠️ Error en la carga de productos: {e}")
    return pd.DataFrame(columns=["nombre", "precio_local", "precio_usd", "tipo_unidad", "unidad", "vendedor", "imagen"])

# Función para subir productos a GitHub
def guardar_producto(nombre, precio_local, precio_usd, tipo_unidad, unidad, vendedor, imagen):
    df = cargar_productos()
    nuevo_producto = pd.DataFrame([[nombre, precio_local, precio_usd, tipo_unidad, unidad, vendedor, imagen]], 
                                  columns=df.columns)
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

# Función para convertir precios
def convertir_a_dolares(precio_local, tasa_cambio=4000):
    return round(precio_local / tasa_cambio, 2)

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
                st.sidebar.success("Registro exitoso. Revisa tu correo.")
                st.rerun()
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
                st.write(f"💰 Precio local: ${producto['precio_local']}")
                st.write(f"💵 Precio en USD: ${producto['precio_usd']}")
                st.write(f"📏 Unidad: {producto['tipo_unidad']} ({producto['unidad']})")
                st.write(f"📧 Vendedor: {producto['vendedor']}")
                
                if st.button(f"🛒 Comprar {producto['nombre']}", key=producto["nombre"]):
                    if st.session_state["user_email"]:
                        st.success("Compra realizada. Revisa tu correo.")
                    else:
                        st.error("⚠️ Debes iniciar sesión para comprar.")

# Sección para agregar nuevos productos
def agregar_producto():
    st.markdown("<h2 style='text-align: center;'>➕ Agregar Nuevo Producto</h2>", unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:  # Centrar el formulario
            with st.form("add_product_form"):
                nombre_producto = st.text_input("📌 Nombre del Producto")
                
                # Precio en moneda local y conversión automática a dólares
                precio_local = st.number_input("💰 Precio en moneda local", min_value=0.1)
                precio_dolares = convertir_a_dolares(precio_local)
                st.write(f"💵 **Precio en USD:** ${precio_dolares}")

                # Tipo de unidad y unidad
                tipo_unidad = st.selectbox("📏 Tipo de Unidad", ["Cantidad", "Peso", "Volumen"])
                unidad = st.text_input("🔢 Unidad (ej. kg, unidades, litros)")
                
                # Imagen (opcional, con una por defecto si no se ingresa una URL)
                imagen_url = st.text_input("🖼️ URL de la Imagen (opcional)")
                imagen_url = imagen_url if imagen_url else "https://via.placeholder.com/150"

                submitted = st.form_submit_button("📤 Publicar Producto")

                if submitted:
                    if nombre_producto and precio_local and unidad and tipo_unidad:
                        guardar_producto(nombre_producto, precio_local, precio_dolares, tipo_unidad, unidad, 
                                         st.session_state["user_email"], imagen_url)
                        st.success(f"✅ **{nombre_producto}** agregado correctamente.")
                        st.experimental_rerun()
                    else:
                        st.error("⚠️ Completa todos los campos obligatorios.")

# Ejecutar la función para agregar productos
agregar_producto()
