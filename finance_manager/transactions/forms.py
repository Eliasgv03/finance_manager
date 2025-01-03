from django import forms
from .models import Transaction, Tag, Currency
from django.utils import timezone

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['type', 'tag', 'currency', 'amount', 'date', 'description']
        widgets = {
            'date': forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Capturamos el usuario desde kwargs.
        super().__init__(*args, **kwargs)

        # Filtrar los tags disponibles según el usuario.
        if user:
            self.fields['tag'].queryset = Tag.objects.filter(user=user)
        else:
            self.fields['tag'].queryset = Tag.objects.none()

        # Inicializar la fecha con el valor actual por defecto.
        self.fields['date'].initial = timezone.now().date()

        # Configurar el campo `currency` como un ModelChoiceField.
        self.fields['currency'] = forms.ModelChoiceField(
            queryset=Currency.objects.all(),
            required=True,
            widget=forms.Select(attrs={'class': 'form-control'}),
            empty_label="Select a currency"  # Texto por defecto en el selector.
        )

        # Asignar la moneda predeterminada del perfil del usuario si está disponible.
        if user and hasattr(user, 'profile') and user.profile.default_currency:
            self.fields['currency'].initial = user.profile.default_currency