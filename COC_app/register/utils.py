from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator


def send_custom_email(subject, template_name, context, to_email):
    html_message = render_to_string(template_name, context)
    plain_message = strip_tags(html_message)
    from_email = 'newprasadsaha@gmail.com'  # Replace with your sending email

    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)