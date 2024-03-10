from django import forms
from .models import Employee

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