from django import forms
from productdetails.models import Product





class ProductAdditionForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=["name","description","price","image","available","category","status"]
        