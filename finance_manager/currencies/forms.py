# forms.py

from django import forms
from .models import Currency

class CurrencyConversionForm(forms.Form):
    from_currency = forms.ModelChoiceField(queryset=Currency.objects.all(), empty_label="Selecciona la moneda de entrada", label="De Moneda")
    to_currency = forms.ModelChoiceField(queryset=Currency.objects.all(), empty_label="Selecciona la moneda de salida", label="A Moneda")
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label="Monto")
