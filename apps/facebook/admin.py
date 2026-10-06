from django.contrib import admin

from .models import Comment, CommentLike, Follow, Post, PostLike

# Register your models here.

admin.site.register(Follow)
admin.site.register(Post)
admin.site.register(PostLike)
admin.site.register(Comment)
admin.site.register(CommentLike)
