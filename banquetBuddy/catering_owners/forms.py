from django import forms
from core.models import Offer

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['title', 'description', 'requirements', 'location']
