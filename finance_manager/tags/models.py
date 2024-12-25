# tags/models.py
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
class Tag(models.Model):
    TAG_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tags')
    name = models.CharField(max_length=50)
    tag_type = models.CharField(max_length=7, choices=TAG_TYPES)
    color = models.CharField(max_length=7, default="#FFFFFF")  
    
    class Meta:
        unique_together = ('user', 'name')  
    
    def __str__(self):
        return f"{self.name} ({self.tag_type})"