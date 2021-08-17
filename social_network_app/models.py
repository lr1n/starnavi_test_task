from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    title = models.CharField(max_length=128)
    content = models.TextField(default='Author will write something soon...')
    created_at = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE,
        related_name='post_likes', blank=True, null=True
    )
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='user_likes', blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
