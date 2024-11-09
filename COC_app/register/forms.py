from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class PasswordResetForm(forms.Form):
    username = forms.CharField(label="Username", required=True)

class UsernameRetrievalForm(forms.Form):
    email = forms.EmailField(label="Email", required=True)
    
class NewPasswordForm(forms.Form):
    email = forms.EmailField(label="Email Address", required=True)
    new_password = forms.CharField(widget=forms.PasswordInput(), label="New Password", required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password", required=True)
