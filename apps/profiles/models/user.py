from django.db import models
from django.contrib.auth.models import AbstractUser
from django.templatetags.static import static

# Create your models here.
class User(AbstractUser):
    
    photo = models.ImageField(upload_to='profiles/photos', null=True, blank=True)
    
    @property
    def photo_url(self):
        if self.photo:
            return self.photo.url

        return static('facebook/img/anonymous_user.webp')

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
    
