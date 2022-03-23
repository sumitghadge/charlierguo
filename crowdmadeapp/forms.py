from dataclasses import field, fields
from django import forms
from crowdmadeapp.models import Product

class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title','description','status','price','product_image']
    
    def __init__(self, *args, **kwargs):
        super(CreateProductForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {'class': 'form-control'}
