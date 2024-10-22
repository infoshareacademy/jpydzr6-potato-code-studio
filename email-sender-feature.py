import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import dotenv
from dotenv import load_dotenv

# MUST INSTALL dotenv !!!! "pip install python-dotenv"
load_dotenv(dotenv_path='.env')
smtp_server = "smtp.wp.pl"
port = 465
sender_email = "biopotato@wp.pl"  # Company's mail
password = os.getenv("mail_password")  # our password, well duh


def send_mail():
    while True:  # I've added this func only here 'cause the rest will be set up by def, one day I hope
        receiver_email = input("Enter receiver email: ")
        if receiver_email == "" or "@" not in receiver_email:  # Checking if the mail is correct
            print("Something went wrong, try again.")
        else:
            break

    subject = input(
        "Enter subject: ")  # In a due time we'll set up def subject name e.g. Confirmation {ID}  for now I leave it like that so any1 can test the functionality
    body = input("Enter your message: ")  # As above, for now I leave it as it is rn  so it can be tested

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Mail sent successfully!")
    except Exception as e:
        print(f"We didn't send your mail! Try again: {e} ")


send_mail()
