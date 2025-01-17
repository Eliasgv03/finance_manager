from django.db import models
from django.contrib.auth.models import User
from currencies.models import Currency
from currencies.services import convert_currency
from decimal import Decimal

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    initial_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 
    default_currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, default=146)

    def __str__(self):
        return self.user.username

    def get_total_balance(self):
        """
        Retorna el balance total mostrado en la interfaz (initial_balance + balance acumulado).
        """
        return self.initial_balance + self.balance
    
    def update_balance_for_new_currency(self):
       """
       Actualiza el saldo del usuario según la nueva moneda predeterminada sin tocar las transacciones.
       """
       if self.default_currency:
        
        previous_currency = self.__class__.objects.get(pk=self.pk).default_currency
        total_balance = self.get_total_balance()

        if self.default_currency != previous_currency:
            try:
               
                converted_balance = convert_currency(
                    from_currency_code=previous_currency.code,
                    to_currency_code=self.default_currency.code,
                    amount=total_balance
                )

                # Actualizamos el saldo con la moneda convertida
                self.balance = Decimal(converted_balance).quantize(Decimal('0.01'))
                self.initial_balance = Decimal(converted_balance).quantize(Decimal('0.01'))
                print(self.initial_balance)
                self.save()  

            except ValueError as e:
                raise ValueError(f"Error al actualizar el saldo del usuario: {e}")
            except Currency.DoesNotExist:
                raise ValueError("La moneda anterior no existe.")
