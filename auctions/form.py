from django import forms
from .models import Listing,Catagory

class MyForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title','description','imageUrl','price','isActive','owner','category',]



class catgoryForm(forms.ModelForm):
    class Meta:
        model = Catagory
        fields = ['categoryName']