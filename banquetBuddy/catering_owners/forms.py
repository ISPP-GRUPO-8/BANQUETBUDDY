import re
from django import forms
from django.core.exceptions import ValidationError
from .models import CateringCompany

class CateringCompanyForm(forms.ModelForm):
    def clean_cif(self):
        cif = self.cleaned_data.get('cif')
        # Expresión regular para validar el formato del CIF
        cif_regex = r'^[A-HJNP-SUVW]{1}\d{7}[0-9A-J]$'
        if not re.match(cif_regex, cif):
            raise forms.ValidationError("The CIF must be in a valid format.")
        return cif
    
    def clean_verification_document(self):
        verification_document = self.cleaned_data.get('verification_document')
        if verification_document:
            if not verification_document.name.endswith('.pdf'):
                raise ValidationError("The file must be a PDF.")
        return verification_document

    class Meta:
        model = CateringCompany
        fields = ["name", "address", "phone_number", "cif","price_plan", "verification_document"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Company name", "class": "rounded-input"}),
            "address": forms.TextInput(attrs={"placeholder": "Company's address", "class": "rounded-input"}),
            "phone_number": forms.TextInput(attrs={"placeholder": "Phone number", "class": "rounded-input"}),
            "cif": forms.TextInput(attrs={"placeholder": "Ex: A1234567J", "class": "rounded-input"}),
            "price_plan": forms.Select(attrs={"class": "rounded-input"}),
            "verification_document": forms.FileInput(attrs={"class": "rounded-input"}),
        }
