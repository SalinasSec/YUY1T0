import smtplib
import ssl
from random import randint
from email.message import EmailMessage

emailEmisor = 'notificacionesclinica12@gmail.com'
clave = 'uamc ianh bugx ywav'


# ------------------ ENVIAR CODIGO ------------------
def enviarCode(destinatario):
    code = str(randint(100000, 999999))
    asunto = "Código de verificación - Clínica"
    cuerpo = "¡Hola!,\nTu código de verificación es: {}\nGracias por registrarte en nuestra clínica.".format(
        code
    )

    enviarCorreo(destinatario, asunto, cuerpo)
    return code


# ------------------ ENVIAR AVISO ------------------
def enviarAviso(destinatario, nombreUsuario):
    asunto = "Avisto de Turno - Clínica"
    cuerpo = "¡Hola {}!,\ntu turno ha sido aceptado.\nPorfavor preséntate a la clínica.".format(
        nombreUsuario
    )
    enviarCorreo(destinatario, asunto, cuerpo)


# ------------------ FUNCION INTERNA ------------------
def enviarCorreo(destinatario, asunto, cuerpo):
    em = EmailMessage()
    em["From"] = emailEmisor
    em["To"] = destinatario
    em["Subject"] = asunto
    em.set_content(cuerpo)

    contexo = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexo) as smtp:
        smtp.login(emailEmisor, clave)
        smtp.send_message(em)
