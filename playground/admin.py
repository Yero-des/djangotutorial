from django.contrib import admin
from .models import Person, Country, Group, Membership

class PersonInline(admin.StackedInline):
    model = Person
    extra = 0

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'shirt_sizes', 'country', 'has_group', 'has_partner', 'partner')
    fieldsets = [
        ('Nombres', {'fields': ['name', 'last_name']}),
        ('Datos adicionales', {'fields': ['shirt_sizes', 'partner', 'country']})
    ]
    
@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'acronym', 'continent', 'independence_date')
    fieldsets = [
        ('Nombres', {'fields': ['name', 'acronym']}),
        ('Datos', {'fields': ['continent', 'independence_date']})        
    ]
    inlines = [PersonInline]
    
@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'date_joined')
    
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass