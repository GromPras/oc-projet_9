from django import forms
from django.forms.models import inlineformset_factory
from .models import Ticket, Review


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

    image = forms.FileField(widget=forms.FileInput())


class NewReviewForm(forms.ModelForm):
    CHOICES = [
        (str(i), "🟊" * i) if i > 0 else (str(i), "☹") for i in range(0, 6)
    ]

    class Meta:
        model = Review
        fields = ["rating", "headline", "body"]
        exclude = ["user"]

    headline = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "text-input", "placeholder": "Titre"}
        ),
    )

    body = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "text-area",
                "placeholder": "Décrivez votre requête en quelques mots",
            }
        ),
    )

    rating = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={"class": "radio-input"}),
        choices=CHOICES,
    )


class NewTicketReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ["user"]


NewTicketReviewFormSet = inlineformset_factory(
    Ticket,
    Review,
    form=NewTicketReviewForm,
    fields=["rating", "headline", "body"],
    extra=1,
)
