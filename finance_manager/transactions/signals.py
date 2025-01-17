from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction as db_transaction
from .models import Transaction
from users.models import UserProfile  

@receiver(post_save, sender=Transaction)
@db_transaction.atomic
def update_balance_on_transaction_save(sender, instance, **kwargs):
   
    user_profile = UserProfile.objects.get(user=instance.user)

    if kwargs.get('created', False):  
        if instance.type == Transaction.INCOME:
            user_profile.balance += instance.amount
        elif instance.type == Transaction.EXPENSE:
            user_profile.balance -= instance.amount
    else: 
        old_transaction = Transaction.objects.get(id=instance.id)

        if old_transaction.type == Transaction.INCOME:
            user_profile.balance -= old_transaction.amount
        elif old_transaction.type == Transaction.EXPENSE:
            user_profile.balance += old_transaction.amount

        if instance.type == Transaction.INCOME:
            user_profile.balance += instance.amount
        elif instance.type == Transaction.EXPENSE:
            user_profile.balance -= instance.amount

    user_profile.save()

@receiver(post_delete, sender=Transaction)
@db_transaction.atomic
def update_balance_on_transaction_delete(sender, instance, **kwargs):
    
    user_profile = UserProfile.objects.get(user=instance.user)

    
    if instance.type == Transaction.INCOME:
        user_profile.balance -= instance.amount
    elif instance.type == Transaction.EXPENSE:
        user_profile.balance += instance.amount

    user_profile.save()
