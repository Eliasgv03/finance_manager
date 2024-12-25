# tags/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Tag

DEFAULT_TAGS = [
    {"name": "Salary", "tag_type": "income", "color": "#4CAF50"},
    {"name": "Investment", "tag_type": "income", "color": "#2196F3"},
    {"name": "Bonus", "tag_type": "income", "color": "#FFC107"},
    {"name": "Groceries", "tag_type": "expense", "color": "#FF5722"},
    {"name": "Rent", "tag_type": "expense", "color": "#E91E63"},
    {"name": "Transportation", "tag_type": "expense", "color": "#9C27B0"},
    {"name": "Entertainment", "tag_type": "expense", "color": "#00BCD4"},
    {"name": "Utilities", "tag_type": "expense", "color": "#795548"},
]

@receiver(post_save, sender=User)
def create_default_tags(sender, instance, created, **kwargs):
    if created:
        for tag in DEFAULT_TAGS:
            Tag.objects.create(user=instance, **tag)
