from django.contrib.auth.models import User
from rest_framework import serializers
from social_network_app.models import Post, Like


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'], password=validated_data['password']
        )
        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'password', 'posts', 'last_login']
        extra_kwargs = {'last_login': {'read_only': True}}


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ['url', 'id', 'author', 'title', 'content', 'created_at']
        extra_kwargs = {
            'author': {'read_only': True}, 'created_at': {'read_only': True}
        }
