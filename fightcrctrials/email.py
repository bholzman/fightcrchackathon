import os
import sendgrid
from sendgrid.helpers.mail import Email, Content, Mail

def send_email(subject, message, reply_to=None):
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email('fightcrchackathon@gmail.com')
    to_email = Email(os.environ.get('FIGHT_CRC_EMAIL'))
    content = Content("text/plain", message)
    mail = Mail(from_email, subject, to_email, content)
    if reply_to is not None:
        mail.set_reply_to(Email(reply_to))
    try:
        return sg.client.mail.send.post(request_body=mail.get())
    except Exception as e:
        print(f"Could not send email to {to_email.email}: {e}\nSUBJECT: {subject}\nMESSAGE: {message}\n")
