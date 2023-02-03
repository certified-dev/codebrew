from django.db import models
from django.contrib.auth.models import AbstractUser, User

from codebin import settings

class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(max_length=10000)
    tags = models.CharField(max_length=100)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)


class UserComment(models.Model):
    posted_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='user_comments', on_delete=models.CASCADE)
    message = models.CharField(max_length=500)
    posted_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(null=True)

    def __str__(self):
        return self.message

class GuestComment(models.Model):
    posted_by = models.CharField(max_length=50)
    post = models.ForeignKey(Post, related_name='guest_comments', on_delete=models.CASCADE)
    message = models.CharField(max_length=500)
    posted_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(null=True)

    def __str__(self):
        return self.message
