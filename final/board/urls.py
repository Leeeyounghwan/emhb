from django.urls import path
from . import views

app_name ='board'

urlpatterns = [
    path('', views.BoardListView.as_view(), name='board_list'),
    path('post/<int:pk>/', views.post_detail_view, name='post_detail'),
    path('write/', views.post_write_view, name='post_write'),
    path('add_comment/<int:pk>', views.post_comment_add_view, name='add_comment')
]
