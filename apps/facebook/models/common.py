from django.conf import settings
from django.db import models


def content_image_path(instance, filename):
    model_name = instance.__class__.__name__.lower()
    return f"facebook/{model_name}s/{filename}"


class CommonContent(models.Model):

    STATUS = {"active": "Active", "deleted": "Deleted", "hidden": "Hidden"}

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="%(class)ss",
        related_query_name="%(app_label)s_%(class)ss",
    )
    description = models.TextField(verbose_name="Contenido")
    status = models.CharField(max_length=20, choices=STATUS)
    image = models.ImageField(
        upload_to=content_image_path, null=True, blank=True, verbose_name="Imagen"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class CommonLike(models.Model):
    REACTIONS = {"like": "Like", "love": "Love", "dislike": "Dislike", "angry": "Angry"}

    user_like = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)ss",
        related_query_name="%(app_label)s_%(class)ss",
    )
    reaction = models.CharField(max_length=10, choices=REACTIONS)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_like} => {self.liked_comment}"

    class Meta:
        abstract = True
