from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):

    @property
    def quantity_followers(self):
        return self.followers.count()
    
    @property
    def quantity_followings(self):
        return self.following.count()
    
    @property
    def quantity_user_likes(self):
        return self.user_likes.count()

    @property
    def quantity_posts(self):
        return self.posts.count()
    
    def __str__(self):
        return self.get_full_name() or self.username
    
