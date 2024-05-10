from django import forms
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView


class SignInForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "text-input", "placeholder": "Nom d'utilisateur"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "password-input", "placeholder": "Mot de passe"}
        )
    )


class SignInView(LoginView):
    form_class = SignInForm
    template_name = "authentication/signin.html"
