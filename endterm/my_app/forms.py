from django import forms
from .models import Shop
class ShopRegisterForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['username', 'email', 'password']
        
    password = forms.CharField(widget=forms.PasswordInput)