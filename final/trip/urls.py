from django.urls import path
from . import views

app_name = 'trip'

urlpatterns = [
    path("", views.main, name='main'),
    path("login/", views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path("register/", views.register, name='register'),
]
