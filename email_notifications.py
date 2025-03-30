import os
from mailersend import emails
import requests
import json
import logging


MAILERSEND_API_KEY = "mlsn.550e6ccae0205cafda6f7e08c7373a1bf04b7e9b62cc1ca7100ba9254c60c034"
MAILERSEND_DOMAIN = "trial-r83ql3pwjevgzw1j.mlsender.net"
MAILERSEND_URL = "https://api.mailersend.com/v1/email"

# Configurar logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Función para cargar plantillas HTML
def cargar_plantilla(nombre_archivo, **kwargs):
    """Carga y personaliza una plantilla HTML."""
    ruta = os.path.join("templates", nombre_archivo)
    if not os.path.exists(ruta):
        logging.error(f"⚠️ Plantilla {nombre_archivo} no encontrada.")
        return None

    with open(ruta, "r", encoding="utf-8") as f:
        plantilla = f.read()

    # Reemplazar variables en la plantilla
    for clave, valor in kwargs.items():
        plantilla = plantilla.replace(f"{{{{ {clave} }}}}", valor)

    return plantilla

# Función genérica para enviar correos
def enviar_correo(destinatario, asunto, mensaje, html_mensaje=None):
    """Envía un correo electrónico usando MailerSend."""
    headers = {
        "Authorization": f"Bearer {MAILERSEND_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "from": {"email": f"no-reply@{MAILERSEND_DOMAIN}", "name": "Marketplace"},
        "to": [{"email": destinatario}],
        "subject": asunto,
        "text": mensaje,
        "html": html_mensaje if html_mensaje else mensaje
    }

    try:
        response = requests.post(MAILERSEND_URL, headers=headers, data=json.dumps(data))
        if response.status_code == 202:
            logging.info(f"✅ Correo enviado a {destinatario}: {asunto}")
        else:
            logging.error(f"❌ Error al enviar correo a {destinatario}: {response.text}")
    except Exception as e:
        logging.error(f"⚠️ Excepción al enviar correo: {e}")

# Correos específicos

def correo_registro(usuario_email, usuario_nombre):
    asunto = "Bienvenido a Marketplace"
    mensaje = f"Hola {usuario_nombre},\n\nGracias por registrarte en nuestro Marketplace."
    html_mensaje = cargar_plantilla("bienvenida.html", usuario_nombre=usuario_nombre)
    enviar_correo(usuario_email, asunto, mensaje, html_mensaje)

def correo_producto_publicado(usuario_email, nombre_producto):
    asunto = "Producto publicado con éxito"
    mensaje = f"Tu producto '{nombre_producto}' ha sido agregado al Marketplace."
    enviar_correo(usuario_email, asunto, mensaje)

def correo_confirmacion_compra(comprador_email, producto, precio):
    asunto = "Confirmación de compra"
    mensaje = f"Has comprado '{producto}' por ${precio}. Espera la confirmación del vendedor."
    html_mensaje = cargar_plantilla("compra_confirmada.html", producto=producto, precio=str(precio))
    enviar_correo(comprador_email, asunto, mensaje, html_mensaje)

def correo_notificacion_vendedor(vendedor_email, comprador, producto):
    asunto = "Nuevo pedido recibido"
    mensaje = f"{comprador} ha comprado tu producto '{producto}'. Coordina la entrega pronto."
    enviar_correo(vendedor_email, asunto, mensaje)

def correo_pago_realizado(usuario_email, producto, monto):
    asunto = "Pago exitoso"
    mensaje = f"Tu pago de ${monto} por '{producto}' ha sido procesado con éxito."
    html_mensaje = cargar_plantilla("pago_realizado.html", producto=producto, monto=str(monto))
    enviar_correo(usuario_email, asunto, mensaje, html_mensaje)

# Nuevo: Restablecimiento de contraseña
def correo_recuperacion_contrasena(usuario_email, enlace_recuperacion):
    asunto = "Restablece tu contraseña"
    mensaje = f"Haz clic en el siguiente enlace para restablecer tu contraseña: {enlace_recuperacion}"
    enviar_correo(usuario_email, asunto, mensaje)

# Nuevo: Confirmación de cuenta
def correo_confirmacion_cuenta(usuario_email, enlace_confirmacion):
    asunto = "Confirma tu cuenta"
    mensaje = f"Para activar tu cuenta, haz clic en el siguiente enlace: {enlace_confirmacion}"
    enviar_correo(usuario_email, asunto, mensaje)

