from django.contrib import admin

from .models import Follow, Post, PostLike

# Register your models here.

admin.site.register(Follow)
admin.site.register(PostLike)
admin.site.register(Post)
