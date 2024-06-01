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
