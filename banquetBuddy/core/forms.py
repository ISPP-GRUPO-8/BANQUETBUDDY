from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Particular, CateringCompany, Employee
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser, CuisineTypeModel, CuisineType


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


class ParticularForm(forms.ModelForm):
    class Meta:
        model = Particular
        fields = ["phone_number", "preferences", "address"]
        widgets = {
            "phone_number": forms.TextInput(
                attrs={"placeholder": "Número de teléfono", "class": "rounded-input"}
            ),
            "preferences": forms.TextInput(
                attrs={"placeholder": "Preferencias", "class": "rounded-input"}
            ),
            "address": forms.TextInput(
                attrs={"placeholder": "Dirección", "class": "rounded-input"}
            ),
        }


class CateringCompanyForm(forms.ModelForm):
    class Meta:
        model = CateringCompany
        fields = ["name", "phone_number", "service_description"]
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Nombre", "class": "rounded-input"}
            ),
            "phone_number": forms.TextInput(
                attrs={"placeholder": "Número de teléfono", "class": "rounded-input"}
            ),
            "service_description": forms.TextInput(
                attrs={
                    "placeholder": "Descripción del servicio",
                    "class": "rounded-input",
                }
            ),
        }

class CateringProfileForm(forms.ModelForm):
    class Meta:
        model = CateringCompany
        fields = ["service_description", "cuisine_types", "logo"]
        widgets = {
            "service_description": forms.Textarea(
                attrs={"placeholder": "Descripción del servicio", "class": "form-control"}
            ),
            "cuisine_types": forms.SelectMultiple(
                choices=CuisineType.choices,
                attrs={"class": "form-control"}
            ),
            "logo": forms.FileInput(
                attrs={"class": "form-control-file"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cuisine_types'].queryset = CuisineTypeModel.objects.all()


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["phone_number", "profession", "experience", "skills"]
        widgets = {
            "phone_number": forms.TextInput(
                attrs={"placeholder": "Número de teléfono", "class": "rounded-input"}
            ),
            "profession": forms.TextInput(
                attrs={"placeholder": "Profesión", "class": "rounded-input"}
            ),
            "experience": forms.TextInput(
                attrs={"placeholder": "Experiencia", "class": "rounded-input"}
            ),
            "skills": forms.TextInput(
                attrs={"placeholder": "Habilidades", "class": "rounded-input"}
            ),
        }


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
