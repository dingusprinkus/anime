from django.db import models
from django.contrib.auth.models import User


# User
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(null=True, blank=True, upload_to="images/users")
    profile_bio = models.CharField(null=True, blank=True, max_length=200)

    def __str__(self):
        return self.username


# Comments
class Comment(models.Model):
    user = (models.ForeignKey(User, on_delete=models.CASCADE),)
    body = models.CharField(max_length=300)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}" f"({self.date_creation: %d-%m-%Y %H:%M}:)" f"{self.body}"


# Replys
class Replys(models.Model):
    content = models.TextField(max_length=300)
    date_creation = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_connect = models.ForeignKey(Comment, on_delete=models.CASCADE)


# Add new Anime
class AddAnime(models.Model):
    anime_name = models.CharField(max_length=100)
    anime_image = models.ImageField(null=False, blank=False, upload_to="images/anime")
    anime_description = models.CharField(max_length=300)

    def __str__(self):
        return self.anime_name
