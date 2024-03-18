import re
from django import forms
from django.core.exceptions import ValidationError
from .models import CateringCompany, CateringService, Menu, Offer


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


class MenuForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(MenuForm, self).__init__(*args, **kwargs)
        if user and hasattr(user, 'CateringCompanyusername'):
            self.fields['cateringservice'].queryset = CateringService.objects.filter(cateringcompany=user.CateringCompanyusername)
            self.fields['cateringservice'].label_from_instance = lambda obj: "%s" % obj.name

    class Meta:
        model = Menu
        fields = ['name', 'description', 'diet_restrictions', 'cateringservice']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'diet_restrictions': forms.TextInput(attrs={'class': 'form-control'}),
            'cateringservice': forms.Select(attrs={'class': 'form-control'}),
        }
  
  
class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['title', 'description', 'requirements', 'location']