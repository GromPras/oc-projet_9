from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


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
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username",)

    username = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "text-input",
                "placeholder": "Nom d'utilisateur",
                "aria-describedby": "usernamehelptext",
            }
        ),
        help_text="Requis. 150 caractères maximum. Uniquement des lettres, nombres et les caractères « @ », « . », « + », « - » et « _ ».",
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "password-input",
                "placeholder": "Mot de passe",
                "aria-describedby": "pwhelptext",
            }
        ),
        help_text="""Votre mot de passe ne peut pas trop ressembler à vos autres informations personnelles.
        Votre mot de passe doit contenir au minimum 8 caractères.
    Votre mot de passe ne peut pas être un mot de passe couramment utilisé.
    Votre mot de passe ne peut pas être entièrement numérique.""",
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "password-input",
                "placeholder": "Confirmation du mot de passe",
                "aria-describedby": "pw2helptext",
            }
        ),
        help_text="Saisissez le même mot de passe que précédemment, pour vérification.",
    )
