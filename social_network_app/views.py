from datetime import datetime
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from rest_framework import generics, permissions, viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from social_network_app.serializers import (
    SignUpSerializer, UserSerializer, PostSerializer, LikeSerializer
)
from social_network_app.permissions import IsAuthorOrReadOnly
from social_network_app.models import Post, Like
from social_network_app.utils import like_analytics


class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': UserSerializer(
                user, context=self.get_serializer_context()
            ).data,
            'message': 'User have created successfully',
        })


class LoginView(generics.GenericAPIView):
    serializer_class = UserSerializer

    @csrf_exempt
    def post(self, request, format=None):
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return Response({
                    'user': UserSerializer(
                        user, context=self.get_serializer_context()
                    ).data,
                    'message': 'User have logged in successfully',
                })

            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@api_view(['GET'])
def analytics(request, date_from, date_to, format=None):
    date_from_iso = datetime.fromisoformat(date_from)
    date_to_iso = datetime.fromisoformat(date_to)
    if request.method == 'GET':
        total_likes = Like.objects.filter(
            created_at__date__range=[date_from_iso, date_to_iso]
        )
        total_likes_serializer = LikeSerializer(total_likes, many=True)
        response = like_analytics(total_likes_serializer)
        return Response(response)
