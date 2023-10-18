from django.urls import path, include
from . import views
urlpatterns = [
    path("packages/", views.packages, name="packages"),
]