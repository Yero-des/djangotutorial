from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Person  

class PersonModelTests(TestCase):
    
    def test_different_shirt_sizes_choices_is_empty(self):
        """
        person.shirt_sizes should return an empty string with a new value
        """
        person = Person(name="Yeromi", last_name="Zavala Castillo", shirt_sizes="XL", country="PE",) 
        
        with self.assertRaises(ValidationError):
            person.full_clean()