from django.conf import settings
from django.db import models
from django.db.models import Exists, OuterRef

from .common import CommonContent, CommonLike
from .post import Post


class PostQuerySet(models.QuerySet):

    def for_user(self, user):
        return self.annotate(
            is_liked=Exists(
                CommentLike.objects.filter(liked_post=OuterRef("pk"), user_like=user)
            )
        )


class Comment(CommonContent):

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    rating = models.PositiveIntegerField()
    objects = PostQuerySet.as_manager()

    def __str__(self):
        return f"{self.user} => {self.post}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["post", "user"], name="unique_comment_by_user"
            )
        ]


class CommentLike(CommonLike):
    liked_comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="likes"
    )

    def __str__(self):
        return f"{self.user_like} => {self.liked_comment}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["liked_comment", "user_like"],
                name="unique_like_comment_by_user",
            )
        ]
