# orders/forms.py
from django import forms

class OrderCreateForm(forms.Form):
    first_name = forms.CharField(label="Имя", max_length=50)
    phone = forms.CharField(label="Телефон", max_length=20)
    address = forms.CharField(label="Адрес доставки", widget=forms.Textarea(attrs={'rows': 3}))