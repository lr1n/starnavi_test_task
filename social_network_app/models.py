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
    post = models.ManyToManyField(Post, related_name='post_likes', blank=True)
    owner = models.ManyToManyField(User, related_name='user_likes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
