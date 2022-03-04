from distutils.command.upload import upload
from pydoc import describe
from pyexpat import model
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'static/media')
    describe = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return self.describe

class PostLike(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)


class PostComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    comment = models.CharField(max_length=500, blank=True)

class FriendRequest(models.Model):
    user_to = models.ForeignKey(User,related_name='user_to',on_delete=models.CASCADE,null=True)
    user_from = models.ForeignKey(User,related_name='user_from',on_delete=models.CASCADE,null=True)
    IsAccepted = models.BooleanField(default=False)
    #OnDate = models.DateTimeField(default=True)