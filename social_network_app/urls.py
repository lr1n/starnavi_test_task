from django.urls import path, include
from social_network_app.views import SignUpUser, UserList

urlpatterns = [
    path('api/sign_up/', SignUpUser.as_view()),
    path('api/users/', UserList.as_view(), name='users')
]
