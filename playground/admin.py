from django.contrib import admin
from .models import Person

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'shirt_sizes', 'country', 'has_partner', 'partner')
    fieldsets = [
        ('Nombres', {'fields': ['name', 'last_name']}),
        ('Datos adicionales', {'fields': ['shirt_sizes', 'country', 'partner']})
    ]