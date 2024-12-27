

# Register your models here.
from django.contrib import admin
from .models import Currency

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'country', 'symbol')  # Campos que se mostrarán en la lista del admin
    search_fields = ('code', 'name', 'country')  # Campos habilitados para la búsqueda
    list_filter = ('country',)  # Filtro por país
    ordering = ('code',)  # Ordenar por código de moneda
    fields = ('code', 'name', 'country', 'symbol')  # Orden de campos en el formulario de edición
