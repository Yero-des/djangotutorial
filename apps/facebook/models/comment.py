from django.conf import settings
from django.db import models

from .common import CommonContent, CommonLike

# class Comment(models.Model):

#     post_comment = models.ForeignKey(
#         Post, on_delete=models.CASCADE, related_name="comments"
#     )
#     user_comment = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
#     )
#     comment = models.TextField(verbose_name="Comentario")
#     comment_image = models.ImageField(
#         upload_to="/facebook/commments", null=True, blank=True, verbose_name="Imagen"
#     )
#     rating = models.PositiveIntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user_comment} => {self.post_comment}"

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=["post_comment", "user_comment"], name="unique_comment_by_user"
#             )
#         ]


# class LikeComment(CommonLike):
#     liked_comment = models.ForeignKey(
#         Comment, on_delete=models.CASCADE, related_name="likes"
#     )

#     def __str__(self):
#         return f"{self.user_like} => {self.liked_comment}"

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=["liked_comment", "user_like"],
#                 name="unique_like_comment_by_user",
#             )
#         ]
