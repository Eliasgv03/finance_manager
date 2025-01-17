from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=UserProfile)
def update_balance_on_currency_change(sender, instance, created, **kwargs):
    """
    Signal para actualizar el saldo del usuario cuando cambia su moneda predeterminada,
    sin modificar las transacciones.
    """
    if not created:  

        previous_currency = sender.objects.filter(pk=instance.pk).values_list('default_currency', flat=True).first()
        
        if previous_currency and instance.default_currency.id != previous_currency:
          
            instance.update_balance_for_new_currency()  
