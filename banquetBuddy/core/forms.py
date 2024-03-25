from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser
from catering_owners.models import Offer



class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.TextInput(
            attrs={"autofocus": True, "placeholder": "Email", "class": "rounded-input"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Contraseña", "class": "rounded-input"}
        )
    )

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label="Last Name")
    email = forms.EmailField(max_length=254, required=True, label="Email")

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

ERROR_CHOICES = [
    ('bug', 'Bug/Error'),
    ('feature_request', 'Feature Request'),
    ('usability_issue', 'Usability Issue'),
    ('other', 'Other'),
]

class ErrorForm(forms.Form):
    name = forms.CharField(max_length=50)
    surname = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    error_type = forms.ChoiceField(choices=ERROR_CHOICES)
    reporter_email = forms.EmailField()


