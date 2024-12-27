
# users/models.py
from django.contrib.auth.models import User
from django.db import models
from currencies.models import Currency 

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    initial_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    default_currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, default=146)

    def __str__(self):
        return self.user.username
