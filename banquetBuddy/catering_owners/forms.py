from django import forms
from core.models import CuisineTypeModel, EnglishLevel, CateringCompany, CuisineType

class EmployeeFilterForm(forms.Form):
    
    EMPTY_CHOICE = ('', 'Any')  # Opción para dejar el campo vacío

    english_level_choices = [EMPTY_CHOICE] + list(EnglishLevel.choices)
    
    english_level = forms.ChoiceField(choices=english_level_choices, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    profession = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Profession'}))
    experience = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Experience'}))
    skills = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Skills'}))
    
    ENGLISH_LEVEL_HIERARCHY = {
        'C2': 7,
        'C1': 6,
        'B2': 5,
        'B1': 4,
        'A2': 3,
        'A1': 2,
        'NONE': 1,
    }
    
    def filter_queryset(self, queryset):
        english_level = self.cleaned_data.get('english_level')
        profession = self.cleaned_data.get('profession')
        experience = self.cleaned_data.get('experience')
        skills = self.cleaned_data.get('skills')

        if english_level:
            hierarchy_value = self.ENGLISH_LEVEL_HIERARCHY.get(english_level, 0)
            print(hierarchy_value)
            queryset = queryset.filter(employee__english_level__in=[clave for clave, valor in self.ENGLISH_LEVEL_HIERARCHY.items() if valor >= hierarchy_value])

        if profession:
            queryset = queryset.filter(employee__profession__icontains=profession)
        if experience:
            queryset = queryset.filter(employee__experience__icontains=experience)
        if skills:
            queryset = queryset.filter(employee__skills__icontains=skills)

        return queryset
    

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

