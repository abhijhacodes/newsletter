import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def add_unsubscription_link(email_body: str, subscription_id: str):
    unsubscribe_endpoint = os.environ['UNSUBSCRIBE_URL']
    unsubscribe_url = f'{unsubscribe_endpoint}/{subscription_id}'

    return f"{email_body} <br/><br/> <a href='{unsubscribe_url}'>Unsubscribe from this newsletter</a>"


def send_email_in_background(email_subject: str, email_body: str, email_reciever: str, allow_unsubscription: bool, subscription_id: str):
    email_sender = os.environ['EMAIL_ID']
    email_password = os.environ['EMAIL_PASSWORD']
    smtp_server = os.environ['SMTP_SERVER']
    smtp_port = os.environ['SMTP_PORT']

    email = MIMEMultipart("alternative")
    email['From'] = email_sender
    email['To'] = email_reciever
    email['Subject'] = email_subject

    if allow_unsubscription:
        email_body = add_unsubscription_link(email_body, subscription_id)

    email.attach(MIMEText(email_body, "plain"))
    email.attach(MIMEText(email_body, "html"))

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=ssl.create_default_context()) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_reciever, email.as_string())
            print(f'Email sent to {email_reciever} successfully 🚀')
    except Exception as e:
        print(f'Error in sending email to {email_reciever}: ${e}')
