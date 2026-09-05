from django.db import models
from django.contrib import admin

# Create your models here.
class Person(models.Model):
    
    SHIRT_SIZES = {
        'S': 'Small',
        'M': 'Medium',
        'L': 'Large'
    }
    
    COUNTRIES = {
        'PE': 'Perú',
        'CO': 'Colombia',
        'CL': 'Chile',
        'BR': 'Brasil',
        'AR': 'Argentina'
    }
    
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    shirt_sizes = models.CharField(max_length=1, choices=SHIRT_SIZES)
    country = models.CharField(max_length=2, choices=COUNTRIES)
    partner = models.OneToOneField('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='pareja')
    
    def __str__(self):
        return f"{self.name} {self.last_name}"
    
    def full_name(self):
        return f"{self.name} {self.last_name}"
    
    @admin.display(
        boolean=True,
        description="Has partner?"
    )
    def has_partner(self):
        return self.partner != None