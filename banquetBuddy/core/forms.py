from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser
from django.contrib.auth import authenticate, get_user_model


from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, get_user_model


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.TextInput(
            attrs={"autofocus": True, "placeholder": "Email", "class": "rounded-input"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "rounded-input"}
        )
    )

    def clean(self):
        email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if email and password:
            User = get_user_model()
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError(
                    "Please enter a correct email and password. Note that both fields may be case-sensitive."
                )

            if not user.check_password(password):
                raise forms.ValidationError(
                    "Please enter a correct email and password. Note that both fields may be case-sensitive."
                )
            elif not user.is_active:
                raise forms.ValidationError(
                    "You must activate your account first. Check your email."
                )
            else:
                self.user_cache = user
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


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
    ("bug", "Bug/Error"),
    ("feature_request", "Feature Request"),
    ("usability_issue", "Usability Issue"),
    ("other", "Other"),
]


class ErrorForm(forms.Form):
    name = forms.CharField(max_length=50)
    surname = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    error_type = forms.ChoiceField(choices=ERROR_CHOICES)
    reporter_email = forms.EmailField()
