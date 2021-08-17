from django.urls import path, include
from social_network_app import views
from social_network_app.api import router

urlpatterns = [
    path('sign_up/', views.SignUpView.as_view()),
    path('', include(router.urls))
]
