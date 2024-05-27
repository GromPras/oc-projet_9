from django import forms


class SearchUsersForm(forms.Form):
    username = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "text-input", "placeholder": "Nom d'utilisateur"}
        ),
    )
