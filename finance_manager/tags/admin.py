# users/admin.py
from django.contrib import admin
from .models import Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'tag_type', 'color', 'user']
    list_filter = ['tag_type']
    search_fields = ['name']
