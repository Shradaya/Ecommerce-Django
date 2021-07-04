from django import forms
from django.contrib.auth.models import User
from ecom.models import Product

class AdminLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())



class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ["title", "slug", "category", "image", "marked_price",
                  "selling_price", "description", "return_policy"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "inputFieldCSS",
                "placeholder": "Enter the product title here..."
            }),
            "slug": forms.TextInput(attrs={
                "class": "inputFieldCSS",
                "placeholder": "Enter the unique slug here..."
            }),
            "category": forms.Select(attrs={
                "class": "inputFieldCSS"
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "inputFieldCSS"
            }),
            "marked_price": forms.NumberInput(attrs={
                "class": "inputFieldCSS",
                "placeholder": "Marked price of the product..."
            }),
            "selling_price": forms.NumberInput(attrs={
                "class": "inputFieldCSS",
                "placeholder": "Selling price of the product..."
            }),
            "description": forms.Textarea(attrs={
                "class": "inputFieldCSS",
                "placeholder": "Description of the product...",
                "rows": 5
            }),
            "return_policy": forms.TextInput(attrs={
                "class": "inputFieldCSS",
                "placeholder": "Enter the product return policy here..."
            }),

        }
