from django import forms

from .models import CateringCompany


class CateringCompanyForm(forms.ModelForm):
    class Meta:
        model = CateringCompany
        fields = ["name", "address", "phone_number", "cif", "verification_document"]
        widgets = {
             "name": forms.TextInput(
                 attrs={"placeholder": "Nombre", "class": "rounded-input"}
             ),
             "phone_number": forms.TextInput(
                 attrs={"placeholder": "Número de teléfono", "class": "rounded-input"}
             ),
         }