from django.urls import path, include
from rest_framework.routers import DefaultRouter
from social_network_app import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('api/sign_up/', views.SignUpUser.as_view()),
    # path('api/users/', views.UserList.as_view(), name='users'),
    path('api/', include(router.urls))
]
