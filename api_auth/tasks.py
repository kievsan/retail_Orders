from django.conf import settings
from django.core.mail import send_mail
from celery import shared_task


@shared_task()
def send_activation_email_example(email, token):
    """Send activation email"""
    subject = 'Welcome to Celery'
    message = 'Hope it helps me'
    sender = settings.EMAIL_FROM
    recipient_list = [email]
    html_message = '<h1>The End</h1>'
    send_mail(subject, message, sender, recipient_list, html_message=html_message)