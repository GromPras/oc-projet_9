from django import forms
from .models import Ticket


class NewTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]
        exclude = ["user"]

    title = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "text-input", "placeholder": "Titre"}
        ),
    )

    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "text-area",
                "placeholder": "Décrivez votre requête en quelques mots",
            }
        ),
    )
