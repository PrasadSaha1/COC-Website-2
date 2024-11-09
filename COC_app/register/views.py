from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, get_user_model, update_session_auth_hash
from django.http import HttpResponseRedirect
from .forms import PasswordResetForm, UsernameRetrievalForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from .utils import send_custom_email  
from django.core.mail import send_mail
from django.conf import settings

def create_account(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account until email verification
            user.save()
            send_verification_email(user, request)
            return render(request, 'register/confirmation_sent.html')
    else:
        form = SignUpForm()

    return render(request, 'register/create_account.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')  # Redirect to the homepage or dashboard after login
    else:
        form = AuthenticationForm()
    
    return render(request, 'register/login.html', {'form': form})


def reset_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            User = get_user_model()
            try:
                user = User.objects.get(username=username)
                # Generate the password reset email context
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                current_site = get_current_site(request)

                context = {
                    'username': user.username,
                    'domain': current_site.domain,
                    'uid': uid,
                    'token': token,
                }
                send_custom_email(
                    subject='Password Reset Request',
                    template_name='register/password_reset_email.html',
                    context=context,
                    to_email=user.email
                )
                messages.success(request, "If the username exists, a password reset link has been sent to the associated email.")
                return redirect('register:password_reset_done')  # Redirect to a "done" page
            except User.DoesNotExist:
                messages.error(request, "Username not found.")
    else:
        form = PasswordResetForm()

    return render(request, 'register/reset_password.html', {'form': form})

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

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('register:login')
    
def confirmation_sent(request):
    return render(request, 'register/confirmation_sent.html')


def change_password_from_email(request):
    uidb64 = request.GET.get('uidb64')
    token = request.GET.get('token')
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)  # Keep the user logged in after password change
                messages.success(request, 'Your password has been successfully updated.')
                return redirect('register:login')
            else:
                error_message = "Passwords do not match. Please try again."
                return render(request, 'register/change_password_from_email.html', {'error_message': error_message})
        
        return render(request, 'register/change_password_from_email.html')
    
    messages.error(request, "The reset link is invalid, possibly because it has expired.")
    return redirect('register:change_password_from_email')

def password_reset_done(request):
    return render(request, "register/password_reset_done.html")

def forgot_username(request):
    if request.method == 'POST':
        form = UsernameRetrievalForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                # Search for users with the provided email
                users = User.objects.filter(email=email)

                if users.exists():
                    # Prepare the username(s) to send (one per line)
                    usernames = [user.username for user in users]
                    message = f"The username(s) associated with your email are:\n\n" + "\n".join(usernames)
                    subject = "Your Username(s)"
                    
                    # Send the email
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,  # Ensure you have a DEFAULT_FROM_EMAIL set in settings.py
                        [email],  # Recipient email address
                    )
                    messages.success(request, "If the email exists, your username(s) have been sent.")
                else:
                    messages.error(request, "No users found with that email address.")
            except Exception as e:
                messages.error(request, f"An error occurred while retrieving your username(s): {e}")

            return render(request, "register/forgot_username.html", {'form': form})
    else:
        form = UsernameRetrievalForm()

    return render(request, "register/forgot_username.html", {'form': form})