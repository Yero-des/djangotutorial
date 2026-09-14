from django.db import models
from django.contrib import admin
from .fields import HandField

class Country(models.Model):
    
    name = models.CharField(max_length=100)
    acronym = models.CharField(max_length=5)
    continent = models.CharField(max_length=200)    
    independence_date = models.DateField()
    
    class Meta:
        verbose_name_plural = 'countries'
        
    def save(self, **kwargs):
        if self.name == 'Israel':
            return
        return super().save(**kwargs)
    
    def __str__(self):
        return f"{self.name} {self.acronym.upper()}"

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
    partner = models.OneToOneField('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='pareja')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'people'
        get_latest_by = 'date_added'
        
    def save(self, **kwargs):
        return super().save(**kwargs)
    
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
    
    @admin.display(
        boolean=True,
        description="Has group?"
    )
    def has_group(self):
        return self.group.exists()
    
class Group(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(Person, through="Membership", related_name='group')    
    
    def save(self, *, force_insert = ..., force_update = ..., using = ..., update_fields = ...):
        return super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
    
    def __str__(self):
        return self.name
    
class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['person', 'group'], name="unique_person_group"
            )
        ]
        
    def __str__(self):
        return f'{self.person} => {self.group}'
