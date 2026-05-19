from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_email(subject, template, context, to_email):
    html_message = render_to_string(template, context)
    send_mail(
        subject=subject,
        message='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[to_email],
        html_message=html_message,
    )