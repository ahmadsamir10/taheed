from django.contrib import admin
from .models import Motorcycle, Client, User, Settings
from django.contrib.auth.models import Group

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'full_name', 'phone', 'is_active', 'is_staff')
    search_fields = ('email', 'username', 'full_name', 'phone')
    list_filter = ('is_active', 'is_staff')
    fieldsets = (
        (None, {
            'fields': ('email', 'username', 'full_name', 'phone', 'password')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
    )
    ordering = ('email',)

class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'phone', 'id_number', 'bike_count', 'is_verified', 'steps', 'created_at')
    search_fields = ('email', 'full_name', 'phone', 'id_number')
    list_filter = ('is_verified', 'steps', 'created_at')

class SingletonAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not self.model.objects.exists()


class MotorcycleAdmin(SingletonAdmin):
    list_display = ('motorcycle_price', 'available_motorcycles', 'soldout_motorcycles', 'total_rental_amount')

class SettingsAdmin(SingletonAdmin):
    list_display = ('agreement_text', 'bank_name', 'bank_account_number')
    
    

