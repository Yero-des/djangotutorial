from django.db import models
from django.conf import settings

class UserConfig(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='config')
    dark_mode = models.BooleanField(default=True)
    
    def __str__(self):
        return f'Config: {self.user.username}'