from django.db import models

# Create your models here.
class User(models.Model):

    ROLES = {
        'admin': 'Administrador',
        'staff': 'Staff',
        'user': 'User'
    }
    
    username = models.CharField(unique=True, max_length=100)
    role = models.CharField(max_length=100, choices=ROLES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def quantity_followers(self):
        return self.followers.count()
    
    @property
    def quantity_followings(self):
        return self.following.count()
    
    @property
    def quantity_user_likes(self):
        return self.user_likes.count()
    
    def __str__(self):
        return self.username
    
class Follow(models.Model):

    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    following_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
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

class Post(models.Model):
    
    STATUS = {
        'active': 'Active',
        'deleted': 'Deleted',
        'hidden': 'Hidden'
    }
    
    title = models.CharField(max_length=100)
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
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
    user_like = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes')
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