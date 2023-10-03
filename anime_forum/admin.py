from django.contrib import admin

from .models import Profile, AddAnime, Comment, Post, Replys

# Register your models here.

admin.site.register(Profile)
admin.site.register(AddAnime)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Replys)
