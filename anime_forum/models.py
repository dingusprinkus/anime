from django.db import models
from django.contrib.auth.models import User


# User
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(null=True, blank=True, upload_to="images/users")
    profile_bio = models.CharField(null=True, blank=True, max_length=200)

    def __str__(self):
        return f"{self.user}"


# Add new Anime
class AddAnime(models.Model):
    anime_name = models.CharField(max_length=100)
    anime_image = models.ImageField(null=False, blank=False, upload_to="images/anime")
    anime_description = models.CharField(max_length=300)

    def __str__(self):
        return self.anime_name


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    image = models.ImageField(null=True, blank=True, upload_to="images/post")
    date_creation = models.DateTimeField(auto_now_add=True)
    body = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title + " | " + str(self.user)


# Comments
class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name="comments", null=True, on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=300)
    likes = models.ManyToManyField(User, related_name="post_like", blank=True)

    date_creation = models.DateTimeField(auto_now_add=True)

    # Track num likes
    def num_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"{self.user}" f"({self.date_creation: %d-%m-%Y %H:%M}:)" f"{self.body}"


# Replys
class Replys(models.Model):
    content = models.TextField(max_length=300)
    date_creation = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_connect = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reply_count = models.ManyToManyField(
        Comment, related_name="reply_count", blank=True
    )

    def num_of_replys(self):
        return self.reply_count.count()

    def __str__(self):
        return f"{self.author} - {self.content} - {self.comment_connect}"
