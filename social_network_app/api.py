
from rest_framework.routers import DefaultRouter
from social_network_app import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'likes', views.LikeViewSet)
