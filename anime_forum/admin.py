from django.contrib import admin

from .models import Profile, AddAnime, Comment

# Register your models here.

admin.site.register(Profile)
admin.site.register(AddAnime)
admin.site.register(Comment)
