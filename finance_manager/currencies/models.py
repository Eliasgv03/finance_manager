# currencies/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)  
    name = models.CharField(max_length=50)  
    country = models.CharField(max_length=100) 
    symbol = models.CharField(max_length=10) 

    def __str__(self):
        return f"{self.name} ({self.code})"


