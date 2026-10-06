from django.conf import settings
from django.db import models
from django.db.models import Count, Exists, OuterRef
from django.templatetags.static import static

from .common import CommonContent, CommonLike


class PostQuerySet(models.QuerySet):

    def for_content(self, user):
        return (
            self.annotate(
                is_liked=Exists(
                    PostLike.objects.filter(liked_post=OuterRef("pk"), user_like=user)
                ),
                followers_count=Count("user__followers", distinct=True),
                likes_count=Count("likes", distinct=True),
            )
            .select_related("user")
            .prefetch_related("comments__user")
        )


class Post(CommonContent):

    objects = PostQuerySet.as_manager()

    @property
    def quantity_likes(self):
        return self.likes.count()

    @property
    def image_url(self):
        if self.image:
            return self.image.url

        return static("facebook/img/post_img_default.webp")


class PostLike(CommonLike):

    liked_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")

    def __str__(self):
        return f"{self.user_like} => {self.liked_post}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["liked_post", "user_like"], name="unique_like_by_user"
            )
        ]
