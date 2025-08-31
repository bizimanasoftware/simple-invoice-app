from django import forms
from django.core.validators import RegexValidator
from .models import CustomUser, Product, Client

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'Username'})
    )
    pin = forms.CharField(
        label="4-Digit PIN",
        widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': '4-Digit PIN'}),
        validators=[RegexValidator(regex=r'^\d{4}$', message='PIN must be exactly 4 digits.')],
        max_length=4
    )
    pin_confirm = forms.CharField(
        label="Confirm PIN",
        widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'Confirm PIN'}),
        max_length=4
    )

    class Meta:
        model = CustomUser
        fields = ('username',)

    def clean(self):
        cleaned_data = super().clean()
        pin = cleaned_data.get("pin")
        pin_confirm = cleaned_data.get("pin_confirm")

        if pin != pin_confirm:
            raise forms.ValidationError("PINs do not match!")
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'Username'}))
    pin = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': '4-Digit PIN'}),
        max_length=4
    )

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'quantity', 'price', 'discount_percent', 'tax_percent']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 2}),
            'quantity': forms.NumberInput(attrs={'class': 'form-input'}),
            'price': forms.NumberInput(attrs={'class': 'form-input'}),
            'discount_percent': forms.NumberInput(attrs={'class': 'form-input'}),
            'tax_percent': forms.NumberInput(attrs={'class': 'form-input'}),
        }
