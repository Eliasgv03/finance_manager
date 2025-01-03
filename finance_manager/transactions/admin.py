

# Register your models here.
from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'tag', 'currency', 'amount', 'date')
    list_filter = ('type', 'tag', 'currency', 'date')
    search_fields = ('user__username', 'tag__name', 'currency__name')
    date_hierarchy = 'date'
