from django.contrib.auth.models import User
from rest_framework import serializers
from social_network_app.models import Post, Like


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'last_login']
        extra_kwargs = {'last_login': {'read_only': True}}


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
