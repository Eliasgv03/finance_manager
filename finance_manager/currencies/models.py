# currencies/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)  # Código de la moneda, por ejemplo: 'USD'
    name = models.CharField(max_length=50)  # Nombre de la moneda, por ejemplo: 'Dólar estadounidense'
    country = models.CharField(max_length=100)  # País correspondiente a la moneda
    symbol = models.CharField(max_length=10)  # Símbolo de la moneda, por ejemplo: '$'

    def __str__(self):
        return f"{self.name} ({self.code})"


