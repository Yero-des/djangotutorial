from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models import Count, Exists, OuterRef
from django.templatetags.static import static

from apps.facebook.models import Follow


class UserQuerySet(models.QuerySet):

    def for_stats(self, user):
        return self.annotate(
            is_following=Exists(
                Follow.objects.filter(followed_user=OuterRef("pk"), following_user=user)
            ),
            followers_count=Count("followers", distinct=True),
            postlikes_count=Count("facebook_postlikes", distinct=True),
            posts_count=Count("facebook_posts", distinct=True),
        )


class UserManager(UserManager.from_queryset(UserQuerySet)):

    def get_queryset(self):
        return super().get_queryset().select_related("config")


# Create your models here.
class User(AbstractUser):

    photo = models.ImageField(
        upload_to="profiles/photos", null=True, blank=True, verbose_name="Foto"
    )

    objects = UserManager()

    @property
    def photo_url(self):
        if self.photo:
            return self.photo.url

        return static("facebook/img/anonymous_user.webp")

    @property
    def quantity_followers(self):
        return self.followers.count()

    @property
    def quantity_followings(self):
        return self.following.count()

    @property
    def quantity_postlikes(self):
        return self.postlikes.count()

    @property
    def quantity_posts(self):
        return self.posts.count()

    def __str__(self):
        return self.get_full_name() or self.username
