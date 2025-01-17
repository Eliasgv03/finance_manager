

# Register your models here.
from django.contrib import admin
from .models import Currency

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'country', 'symbol')  
    search_fields = ('code', 'name', 'country') 
    list_filter = ('country',)  
    ordering = ('code',)  
    fields = ('code', 'name', 'country', 'symbol') 
