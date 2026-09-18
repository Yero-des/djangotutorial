from django.db import models
from django.conf import settings

class Follow(models.Model):

    followed_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followers")
    following_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'followers'
        constraints = [
            models.UniqueConstraint(
                fields=['followed_user', 'following_user'], name="unique_follow_by_user"
            )
        ]
        
    def __str__(self):
        return f'{self.following_user} => {self.followed_user}'

