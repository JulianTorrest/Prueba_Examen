import os
from mailersend import emails

MAILERSEND_API_KEY = "mlsn.550e6ccae0205cafda6f7e08c7373a1bf04b7e9b62cc1ca7100ba9254c60c034"

def enviar_correo(destinatario, asunto, mensaje):
    mailer = emails.NewEmail(MAILERSEND_API_KEY)
    
    mail = {
        "from": {"email": "mensaje@trial-r83ql3pwjevgzw1j.mlsender.net", "name": "Marketplace"},
        "to": [{"email": destinatario}],
        "subject": asunto,
        "text": mensaje
    }

    response = mailer.send(mail)
    return response
