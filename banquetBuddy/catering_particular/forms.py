from django import forms

from .models import Particular


class ParticularForm(forms.ModelForm):
    class Meta:
        model = Particular
        fields = ["phone_number", "preferences", "address"]
        widgets = {
            "phone_number": forms.TextInput(
                attrs={"placeholder": "Phone number", "class": "rounded-input"}
            ),
            "preferences": forms.TextInput(
                attrs={"placeholder": "Preferences", "class": "rounded-input"}
            ),
            "address": forms.TextInput(
                attrs={"placeholder": "Adrress", "class": "rounded-input"}
            ),
        }
