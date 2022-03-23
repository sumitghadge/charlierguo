from dataclasses import field, fields
from django import forms
from crowdmadeapp.models import Product

class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title','description','status','price']
