# orders/forms.py
# orders/forms.py
from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
            'address': 'Адрес доставки',
            'postal_code': 'Почтовый индекс',
            'city': 'Город',
        }


# class OrderCreateForm(forms.Form):
#     first_name = forms.CharField(label="Имя", max_length=50)
#     phone = forms.CharField(label="Телефон", max_length=20)
#     address = forms.CharField(label="Адрес доставки", widget=forms.Textarea(attrs={'rows': 3}))