from django import forms

from .models import Particular

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
