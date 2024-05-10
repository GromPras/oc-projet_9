from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy


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


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "text-input", "placeholder": "Nom d'utilisateur"}
        ),
        help_text="Requis. 150 caractères maximum. Uniquement des lettres, nombres et les caractères « @ », « . », « + », « - » et « _ ».",
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "password-input", "placeholder": "Mot de passe"}
        ),
        help_text="""Votre mot de passe ne peut pas trop ressembler à vos autres informations personnelles.
        Votre mot de passe doit contenir au minimum 8 caractères.
    Votre mot de passe ne peut pas être un mot de passe couramment utilisé.
    Votre mot de passe ne peut pas être entièrement numérique.""",
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "password-input",
                "placeholder": "Confirmation du mot de passe",
            }
        ),
        help_text="Saisissez le même mot de passe que précédemment, pour vérification.",
    )


class SignInView(LoginView):
    form_class = SignInForm
    template_name = "authentication/signin.html"


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("signin")
    template_name = "authentication/signup.html"
