# utils/mailer.py
from flask_mail import Message
from flask import current_app
from app import mail

def enviar_correo(destinatario, asunto, cuerpo):
    msg = Message(asunto,
                  recipients=[destinatario],
                  body=cuerpo,
                  sender=current_app.config['MAIL_USERNAME'])
    mail.send(msg)
