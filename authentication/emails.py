import threading
from django.core.mail import send_mail
from django.conf import settings


class EmailThread(threading.Thread):
    def __init__(self, subject, message, recipient_list):
        self.subject = subject
        self.message = message
        self.recipient_list = recipient_list
        threading.Thread.__init__(self)

    def run(self):
        send_mail(
            self.subject,
            self.message,
            settings.EMAIL_HOST_USER,
            self.recipient_list,
            fail_silently=False,
        )


def send_verification_email(username, email):
    subject = 'Welcome to Our Platform'
    message = f'Hello {username},\n\nWelcome to our platform! Thank you for signing up.\n\nBest regards,\nThe Team'
    recipient_list = [email]
    
    EmailThread(subject, message, recipient_list).start()
