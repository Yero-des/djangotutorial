from django.contrib import admin
from .models import Follow, Post, Like
# Register your models here.

admin.site.register(Follow)
admin.site.register(Like)
admin.site.register(Post)