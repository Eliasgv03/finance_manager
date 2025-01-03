from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'initial_balance', 'balance', 'total_balance')

    def total_balance(self, obj):
        return obj.get_total_balance()
    total_balance.short_description = 'Total Balance'
