# tags/serializers.py
from rest_framework import serializers
from .models import Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'type']  # Incluye los campos que deseas mostrar