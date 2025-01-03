from django.db import models
from django.conf import settings
from decimal import Decimal
from django.contrib.auth.models import User
from currencies.services import convert_currency
from django.core.exceptions import ValidationError
from tags.models import Tag
from currencies.models import Currency

class Transaction(models.Model):
    EXPENSE = 'expense'
    INCOME = 'income'
    TRANSACTION_TYPES = [
        (EXPENSE, 'Expense'),
        (INCOME, 'Income'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)
    tag = models.ForeignKey('tags.Tag', on_delete=models.CASCADE, related_name='transactions')
    currency = models.ForeignKey('currencies.Currency', on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.type} - {self.amount} {self.currency}"

    def save(self, *args, **kwargs):
        """
        Guardar transacciones y asegurar conversiones consistentes.
        """
        user_profile = getattr(self.user, 'profile', None)
    
        if user_profile and self.currency != user_profile.default_currency:
            try:
               # Conversión de moneda si es necesario
                converted_amount = convert_currency(
                  from_currency_code=self.currency.code,
                  to_currency_code=user_profile.default_currency.code,
                  amount=self.amount
                )
                self.amount = Decimal(converted_amount).quantize(Decimal('0.01'))
                self.currency = user_profile.default_currency
            except ValueError as e:
                raise ValidationError(f"Error en la conversión de moneda: {e}")
  
        super().save(*args, **kwargs)

    
    def clean(self):
        """
        Validaciones personalizadas.
        """
        if self.amount <= 0:
            raise ValidationError("El monto de la transacción debe ser positivo.")

    class Meta:
        ordering = ['-date']
