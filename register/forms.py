from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]


class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={}
        )
    )


class ChangePasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={}
        ))
