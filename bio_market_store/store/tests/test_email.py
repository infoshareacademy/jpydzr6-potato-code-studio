from django.test import TestCase
from django.core.mail import send_mail


class EmailTest(TestCase):
    def test_send_email(self):
        subject = "Testowy e-mail"
        message = "losowa wiadomość"
        from_email = "biopotato@wp.pl"
        recipient_list = ["charkiewicz.jakubb@gmail.com"]

        mail_send = send_mail(
            subject, message, from_email, recipient_list, fail_silently=False
        )

        self.assertEqual(mail_send, 1, "mail has not been sent :(")
