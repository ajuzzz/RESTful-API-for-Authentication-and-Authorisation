from django.contrib import admin
from django.urls import path
from .views import UserRegisterView, LoginView, UserView, LogoutView

urlpatterns = [
    path('register', UserRegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view())
]