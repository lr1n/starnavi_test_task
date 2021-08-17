from django.contrib.auth.models import User
from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from social_network_app.serializers import (
    SignUpSerializer, UserSerializer, PostSerializer
)
from social_network_app.permissions import IsAuthorOrReadOnly
from social_network_app.models import Post, Like


class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'message': 'User have created successfully',
        })


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
