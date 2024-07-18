from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class UserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


class ContactForm(forms.Form):
    sender_name = forms.CharField(max_length=255, label="Nome")

    sender_email = forms.EmailField(max_length=1024, label="E-mail")

    subject = forms.CharField(max_length=255, label="Assunto")

    message = forms.CharField(
        max_length=1024 * 10, label="Mensagem", widget=forms.Textarea
    )
