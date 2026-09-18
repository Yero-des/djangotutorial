from django.db import models
from django.conf import settings

class Post(models.Model):
    
    STATUS = {
        'active': 'Active',
        'deleted': 'Deleted',
        'hidden': 'Hidden'
    }
    
    title = models.CharField(max_length=100)
    body = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS)
    
    def __str__(self):
        return self.title
    
    @property
    def quantity_likes(self):
        return self.likes.count()
    
class Like(models.Model):
    
    REACTIONS = {
        'like': 'Like',
        'love': 'Love',
        'dislike': 'Dislike',
        'angry': 'Angry'
    }
    
    liked_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user_like = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_likes')
    reaction = models.CharField(max_length=10, choices=REACTIONS)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.liked_postuser_like} => {self.liked_post}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['liked_post', 'user_like'], name="unique_like_by_user"
            )
        ]