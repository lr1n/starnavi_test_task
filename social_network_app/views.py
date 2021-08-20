from datetime import datetime
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from rest_framework import generics, permissions, viewsets, status
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes as dec_perm_classes
from rest_framework.response import Response
from social_network_app.serializers import (
    SignUpSerializer, UserSerializer, PostSerializer,
    LikeSerializer, ProfileSerializer
)
from social_network_app.permissions import IsOwnerOrReadOnly
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


@csrf_exempt
@api_view(['POST'])
@dec_perm_classes([permissions.AllowAny])
def login_view(request, format=None):
    data = request.data
    username = data.get('username', None)
    password = data.get('password', None)
    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            login(request, user)
            return Response(status=status.HTTP_200_OK)

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
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@api_view(['GET'])
def analytics(request, date_from, date_to, format=None):
    date_from_iso = datetime.fromisoformat(date_from)
    date_to_iso = datetime.fromisoformat(date_to)
    # We are getting all likes from 'date_from' to 'date_to'.
    total_likes = Like.objects.filter(
        created_at__date__range=[date_from_iso, date_to_iso]
    )
    total_likes_serializer = LikeSerializer(total_likes, many=True)
    response = like_analytics(total_likes_serializer)
    return Response(response)


@api_view(['GET'])
def last_activity(request, format=None):
    user = request.user
    profile = request.user.profile
    user_serializer = UserSerializer(user)
    profile_serializer = ProfileSerializer(profile)
    username = user_serializer.data['username']
    last_login = user_serializer.data['last_login']
    last_activity = profile_serializer.data['last_activity']
    response = {
        username: {'last_login': last_login, 'last_activity': last_activity}
    }
    return Response(response)


@api_view(['POST', 'DELETE'])
def like_post(request, pk):
    user = request.user

    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        like, created = Like.objects.get_or_create(owner=user, post=post)
        if not created:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_201_CREATED)

    if request.method == 'DELETE':
        Like.objects.filter(owner=user, post=post).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
