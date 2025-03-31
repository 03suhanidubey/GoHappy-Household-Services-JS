from flask_mail import Message, Mail
from flask import current_app 

mail=Mail()

def send_email(subject, to, body=None):

    sender='admin@app.com'

    with current_app.app_context():
        msg = Message(subject, sender=sender, recipients=[to], html=body)
        mail.send(msg)
