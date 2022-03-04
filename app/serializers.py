from dataclasses import field
from matplotlib.pyplot import cla
from rest_framework import serializers
from .models import *

class UserSerilizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = "__all__"

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = "__all__"