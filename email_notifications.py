import os
from mailersend import emails
from config import MAILERSEND_API_KEY, MAILERSEND_DOMAIN

MAILERSEND_API_KEY = "mlsn.550e6ccae0205cafda6f7e08c7373a1bf04b7e9b62cc1ca7100ba9254c60c034"

def enviar_correo(destinatario, asunto, mensaje):
    """ Envía un correo electrónico usando MailerSend """
    mailer = emails.NewEmail(MAILERSEND_API_KEY)
    
    mail = {
        "from": {"email": f"no-reply@trial-r83ql3pwjevgzw1j.mlsender.net", "name": "Marketplace"},
        "to": [{"email": destinatario}],
        "subject": asunto,
        "text": mensaje
    }

    response = mailer.send(mail)
    return response

def correo_registro(usuario_email, usuario_nombre):
    asunto = "Bienvenido a Marketplace"
    mensaje = f"Hola {usuario_nombre},\n\nGracias por registrarte en nuestro Marketplace."
    enviar_correo(usuario_email, asunto, mensaje)

def correo_producto_publicado(usuario_email, nombre_producto):
    asunto = "Producto publicado con éxito"
    mensaje = f"Tu producto '{nombre_producto}' ha sido agregado al Marketplace."
    enviar_correo(usuario_email, asunto, mensaje)

def correo_confirmacion_compra(comprador_email, producto, precio):
    asunto = "Confirmación de compra"
    mensaje = f"Has comprado '{producto}' por ${precio}. Espera la confirmación del vendedor."
    enviar_correo(comprador_email, asunto, mensaje)

def correo_notificacion_vendedor(vendedor_email, comprador, producto):
    asunto = "Nuevo pedido recibido"
    mensaje = f"{comprador} ha comprado tu producto '{producto}'. Coordina la entrega pronto."
    enviar_correo(vendedor_email, asunto, mensaje)

def correo_pago_realizado(usuario_email, producto, monto):
    asunto = "Pago exitoso"
    mensaje = f"Tu pago de ${monto} por '{producto}' ha sido procesado con éxito."
    enviar_correo(usuario_email, asunto, mensaje)
