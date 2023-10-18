from django.urls import path
from . import views

app_name = 'trip'

urlpatterns = [
    path('',views.index, name = "index"),
    path('about/',views.about, name='about'),
    path('blog/',views.blog, name='blog'),
    path('contact/',views.contact, name='contact'),
    path('elements/',views.elements, name='elements'),
    path('main/',views.main, name='main'),
    path('packages/',views.packages, name='packages'),
    path('single_blog/',views.single_blog, name='single_blog'),
    
    #댓글
    path('comment/', views.comment, name='comment'), 
]
