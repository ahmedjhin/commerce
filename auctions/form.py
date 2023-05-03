from django import forms
from .models import Listing

class MyForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title','description','imageUrl','price','isActive','owner','category',]


