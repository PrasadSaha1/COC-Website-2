from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.models import User

from .utils import send_custom_email  # Import the modular email function
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from .forms import PasswordResetForm


def send_verification_email(user, request):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    current_site = get_current_site(request)

    context = {
        'user': user,
        'domain': current_site.domain,
        'uid': uid,
        'token': token,
    }

    send_custom_email(
        subject='Activate your account',
        template_name='register/verification_email.html',
        context=context,
        to_email=user.email
    )

def reset_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                # Generate the password reset email context
                context = {
                    'email': email,
                    'reset_link': 'your_reset_link_here',  # Add logic for reset link generation
                }
                send_custom_email(
                    subject='Password Reset Request',
                    template_name='main/password_reset_email.html',
                    context=context,
                    to_email=email
                )
                messages.success(request, "If that email address exists, a password reset link has been sent.")
                return redirect('password_reset_done')  # Redirect to a "done" page
            else:
                messages.error(request, "Email address not found.")
    else:
        form = PasswordResetForm()

    return render(request, 'main/reset_password.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')  # Redirect to login page after successful activation
    else:
        return render(request, 'register/activation_invalid.html')  # Show invalid token message



def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account until email verification
            user.save()
            send_verification_email(user, request)
            return render(request, 'register/confirmation_sent.html')
    else:
        form = RegisterForm()
    return render(request, 'register/register.html', {'form': form})


