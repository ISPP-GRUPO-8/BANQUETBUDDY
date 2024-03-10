from django import forms
from core.models import EnglishLevel

class EmployeeFilterForm(forms.Form):
    
    EMPTY_CHOICE = ('', 'Any')  # Opción para dejar el campo vacío

    english_level_choices = [EMPTY_CHOICE] + list(EnglishLevel.choices)
    
    english_level = forms.ChoiceField(choices=english_level_choices, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    profession = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Profession'}))
    experience = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Experience'}))
    skills = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Skills'}))
    
    def filter_queryset(self, queryset):
        english_level = self.cleaned_data.get('english_level')
        profession = self.cleaned_data.get('profession')
        experience = self.cleaned_data.get('experience')
        skills = self.cleaned_data.get('skills')

        if english_level:
            queryset = queryset.filter(employee__english_level=english_level)
        if profession:
            queryset = queryset.filter(employee__profession__icontains=profession)
        if experience:
            queryset = queryset.filter(employee__experience__icontains=experience)
        if skills:
            queryset = queryset.filter(employee__skills__icontains=skills)

        return queryset