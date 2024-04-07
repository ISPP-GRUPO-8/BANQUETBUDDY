import re
from django import forms
from django.core.exceptions import ValidationError

from core.models import EnglishLevel
from .models import CateringCompany, CateringService, Menu, Offer, Plate, Question, Form


class CateringCompanyForm(forms.ModelForm):

    def clean_cif(self):
        cif = self.cleaned_data.get("cif")
        # Expresión regular para validar el formato del CIF
        cif_regex = r"^[A-HJNP-SUVW]{1}\d{7}[0-9A-J]$"
        if not re.match(cif_regex, cif):
            raise forms.ValidationError("The CIF must be in a valid format.")
        return cif

    def clean_verification_document(self):
        verification_document = self.cleaned_data.get("verification_document")
        if verification_document:
            if not verification_document.name.endswith(".pdf"):
                raise ValidationError("The file must be a PDF.")
        return verification_document

    class Meta:
        model = CateringCompany
        fields = [
            "name",
            "address",
            "phone_number",
            "cif",
            "verification_document",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Company name", "class": "form-control"}
            ),
            "address": forms.TextInput(
                attrs={"placeholder": "Company's address", "class": "form-control"}
            ),
            "phone_number": forms.TextInput(
                attrs={"placeholder": "Phone number", "class": "form-control"}
            ),
            "cif": forms.TextInput(
                attrs={"placeholder": "Ex: A1234567J", "class": "form-control"}
            ),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["name"].required = True
            self.fields["address"].required = False
            self.fields["phone_number"].required = True
            self.fields["cif"].required = False
            self.fields["verification_document"].required = False


class MenuForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(MenuForm, self).__init__(*args, **kwargs)
        if user and hasattr(user, "CateringCompanyusername"):
            self.fields["cateringservice"].queryset = CateringService.objects.filter(
                cateringcompany=user.CateringCompanyusername
            )
            self.fields["cateringservice"].label_from_instance = (
                lambda obj: "%s" % obj.name
            )

    class Meta:
        model = Menu
        fields = ["name", "description", "diet_restrictions", "cateringservice"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "diet_restrictions": forms.TextInput(attrs={"class": "form-control"}),
            "cateringservice": forms.Select(attrs={"class": "form-control"}),
        }


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ["title", "description", "requirements", "location"]


class EmployeeFilterForm(forms.Form):

    EMPTY_CHOICE = ("", "Any")  # Opción para dejar el campo vacío

    english_level_choices = [EMPTY_CHOICE] + list(EnglishLevel.choices)

    english_level = forms.ChoiceField(
        choices=english_level_choices,
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    profession = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Profession"}
        ),
    )
    experience = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Experience"}
        ),
    )
    skills = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Skills"}
        ),
    )

    ENGLISH_LEVEL_HIERARCHY = {
        "C2": 7,
        "C1": 6,
        "B2": 5,
        "B1": 4,
        "A2": 3,
        "A1": 2,
        "NONE": 1,
    }

    def filter_queryset(self, queryset):
        english_level = self.cleaned_data.get("english_level")
        profession = self.cleaned_data.get("profession")
        experience = self.cleaned_data.get("experience")
        skills = self.cleaned_data.get("skills")

        if english_level:
            hierarchy_value = self.ENGLISH_LEVEL_HIERARCHY.get(english_level, 0)
            print(hierarchy_value)
            queryset = queryset.filter(
                employee__english_level__in=[
                    clave
                    for clave, valor in self.ENGLISH_LEVEL_HIERARCHY.items()
                    if valor >= hierarchy_value
                ]
            )

        if profession:
            queryset = queryset.filter(employee__profession__icontains=profession)
        if experience:
            queryset = queryset.filter(employee__experience__icontains=experience)
        if skills:
            queryset = queryset.filter(employee__skills__icontains=skills)

        return queryset


class CateringServiceFilterForm(forms.Form):
    def __init__(self, catering_company, *args, **kwargs):
        super(CateringServiceFilterForm, self).__init__(*args, **kwargs)
        self.fields["catering_service"] = forms.ModelChoiceField(
            queryset=CateringService.objects.filter(cateringcompany=catering_company),
            required=False,
        )


class CateringServiceForm(forms.ModelForm):
    class Meta:
        model = CateringService
        fields = ["name", "description", "location", "capacity", "price"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "capacity": forms.NumberInput(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
        }

from django import forms
from .models import Plate, Menu

class PlateForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(PlateForm, self).__init__(*args, **kwargs)
        if user and hasattr(user, "CateringCompanyusername"):
            self.fields["menu"].queryset = Menu.objects.filter(
                cateringcompany=user.CateringCompanyusername
            )
            self.fields["menu"].label_from_instance = lambda obj: "%s" % obj.name

    class Meta:
        model = Plate
        fields = ["name", "description", "price", "menu"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "menu": forms.Select(attrs={"class": "form-control"}),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']
class FormForm(forms.ModelForm):
    class Meta:
        model = Form
        fields = ['catering', 'name', 'questions']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None) 
        super(FormForm, self).__init__(*args, **kwargs)

        if user:
            catering_company = CateringCompany.objects.filter(user=user).first()
            if catering_company:
                self.fields['catering'].queryset = CateringService.objects.filter(cateringcompany=catering_company)

        self.fields['questions'].widget.attrs['class'] = 'form-control'
        self.fields['questions'].widget = forms.CheckboxSelectMultiple()
        self.fields['questions'].queryset = Question.objects.filter(catering = CateringCompany.objects.get(name = user))