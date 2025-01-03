from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile
from transactions.models import Transaction
from currencies.services import convert_currency
from decimal import Decimal

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



@receiver(post_save, sender=UserProfile)
def update_transactions_on_currency_change(sender, instance, created, **kwargs):
    """
    Signal para actualizar las transacciones del usuario cuando cambia su moneda predeterminada.
    """
    if not created:  # Solo ejecutamos esto si el usuario ya existe
        # Obtener la moneda predeterminada anterior
        previous_currency = sender.objects.filter(pk=instance.pk).values_list('default_currency', flat=True).first()
        
        if previous_currency and instance.default_currency.id != previous_currency:
            # Recorrer todas las transacciones del usuario
            transactions = Transaction.objects.filter(user=instance)
            for transaction in transactions:
                try:
                    # Convertir el monto a la nueva moneda predeterminada
                    converted_amount = convert_currency(
                        from_currency_code=transaction.currency.code,
                        to_currency_code=instance.default_currency.code,
                        amount=transaction.amount
                    )
                    transaction.amount = Decimal(converted_amount).quantize(Decimal('0.01'))
                    transaction.currency = instance.default_currency
                    transaction.save()
                except ValueError as e:
                    raise ValueError(f"Error en la conversión de transacción {transaction.id}: {e}")
