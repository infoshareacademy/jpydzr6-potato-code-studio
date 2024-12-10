import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from random import  randint

# import dotenv
# from dotenv import load_dotenv

# MUST INSTALL dotenv !!!!! "pip install python-dotenv"
# load_dotenv(dotenv_path='.env')
smtp_server = "smtp.wp.pl"
port = 465
sender_email = "biopotato@wp.pl"  # Company's mail
# password = os.getenv("mail_password")  # our password, well duh load it using dotenv library and password from .env
password = "wpisz hasło"

def send_mail(basket, total_price):
    email = input("Podaj e-mail, a wyślemy Tobie potwierdzenie zakupu.\nTwój e-mail: ").strip()
    while True:

        if email == "" or "@" not in email:
            print("Something went wrong, try again.")
            email = input("Podaj e-mail, a wyślemy Tobie potwierdzenie zakupu.\nTwój e-mail: ").strip()
        else:
            receiver_email = email
            break

    if not basket:
        basket_details = "Koszyk jest pusty."
    else:
        basket_details = "\n".join(
            f"- {item['name_tag']}"
            for item in basket
        )
    mess_confirmation = (
        f"Dziękujemy za zakupy!\n\n"
        f"Twoje produkty:\n{basket_details}\n\n"
        f"Łączna zapłacona kwota: {total_price} PLN\n\n"
        f"Zapraszamy ponownie!"
    )
    id_generator = randint(10000, 99999)
    subject = f"Potwierdzenie zakupu #{id_generator}"
    body = mess_confirmation

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
            print("Potwierdzenie zostało wysłane na Twojego maila, dziękujemy za zakupy!")
    except Exception as e:
        print(f"We didn't send your mail! Try again: {e} ")



