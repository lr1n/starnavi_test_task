from django.urls import path, include
from social_network_app import views
from social_network_app.api import router

urlpatterns = [
    path('sign_up/', views.SignUpView.as_view()),
    path('login/', views.login_view),
    path('analytics/<str:date_from>&<str:date_to>/', views.analytics),
    path('last_activity/', views.last_activity),
    path('like/<int:pk>/', views.like_post),
    path('', include(router.urls))
]
