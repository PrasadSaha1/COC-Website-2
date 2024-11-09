from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, update_session_auth_hash
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User


@login_required(login_url='/register/')
def home(response):
    return render(response, "main/home.html", {})


@login_required(login_url="/register/")
def settings(response):
    return render(response, "main/settings.html", {})


@login_required(login_url="/register/")
def logout_view(request):
    logout(request)

    return redirect("register")


@login_required(login_url="/register/")
def change_username(request):
    if request.method == 'POST':
        new_username = request.POST.get('new_username')
        password = request.POST.get('password')

        if new_username and password:
            # Check if the username is already taken
            if User.objects.filter(username=new_username).exists():
                return JsonResponse({'status': 'taken'})

            # Check if the provided password is correct
            user = authenticate(request, username=request.user.username, password=password)
            if user is None:
                return JsonResponse({'status': 'incorrect_password'})

            # Change the username and save
            request.user.username = new_username
            request.user.save()
            messages.success(request, 'Username successfully changed.')
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error'})
    return render(request, 'main/change_username.html')


@login_required(login_url="/register/")
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Check if the current password is correct
        user = authenticate(request, username=request.user.username, password=current_password)
        if user is None:
            return JsonResponse({'status': 'incorrect_password'})

        # Check if the new passwords match
        if new_password != confirm_password:
            return JsonResponse({'status': 'password_mismatch'})

        # Update the password and save the user
        user.set_password(new_password)
        user.save()

        # Keep the user logged in after changing the password
        update_session_auth_hash(request, user)

        messages.success(request, 'Password successfully changed.')
        return JsonResponse({'status': 'success'})

    return render(request, "main/change_password.html", {})
