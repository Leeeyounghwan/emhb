from django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static
from .testviews import test
app_name = 'trip'
urlpatterns = [
    #마이페이지 by 준경
    path('mypage/profile/', views.profile, name='profile'),
    path('mypage/mytopics/', views.mytopics, name='mytopics'),
    path('mypage/myfeadback/', views.myfeadback, name='myfeadback'),
    path('mypage/like_schedule/', views.like_schedule, name='like_schedule'),
    path('mypage/chatting_room/', views.chatting_room, name='chatting_room'),

    
    
    # 관리자 페이지 관련 urlpatterns by 영환
    path("admin_page/", views.admin_page, name="admin_page"),
    path("admin_page/create_product", views.create_product, name="create_product"),
    path("admin_page/update_product/<int:package_id>", views.update_product, name="update_product"),
    path("admin_page/product_management", views.product_management, name="product_management"),
    path("admin_page/deleted_product", views.deleted_product, name="deleted_product"),
    path("admin_page/delete_cancel/<int:package_id>", views.delete_cancel, name="delete_cancel"),
    path("admin_page/order_inquiry", views.order_inquiry, name="order_inquiry"),
    path("admin_page/delivery_tracking", views.delivery_tracking, name="delivery_tracking"),
    path("admin_page/return_management", views.return_management, name="return_management"),
    path("admin_page/report_detail", views.report_detail, name="report_detail"),
    path("admin_page/report_detail/<int:id>", views.view_report_detail, name="view_report_detail"),
    path("admin_page/report_complete/<int:id>", views.report_complete, name="report_complete"),
    path("admin_page/blacklist_management", views.blacklist_management, name="blacklist_management"),
    path("admin_page/black_cancel/<int:blacklist_id>", views.black_cancel, name="black_cancel"),
    # 관리자 페이지 관련 urlpatterns 종료

    #by 건영
    path('',views.index, name = "index"),
    path('about/',views.about, name='about'),
    path('blog/',views.blog, name='blog'),
    path('contact/',views.contact, name='contact'),
    path('elements/',views.elements, name='elements'),
    path('main/',views.main, name='main'),
  
    # 여행 상품 페이지 By 수현
    path('packages/',views.packages, name='packages'),
    path('single_blog/<int:post_id>/',views.single_blog, name='single_blog'), 
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('single_blog/',views.single_blog, name='single_blog'),

    # 로그인, 회원가입 페이지 by 문정
    path('login/', views.user_login, name = 'login'),
    path('logout/', views.user_logout, name= 'logout'),
    path('register/', views.register, name='register'),
    
    #CHATBOT BY 영민
    path('chatbot/', views.chatbot, name='chatbot'),
    path('chatapi/<str:question>', views.chatapi, name='chatapi'),
    
    #실시간 채팅 BY 영민
    path('chat/', views.chatting, name='chatting'),
    path('chat/<str:room_name>/', views.room, name='room'),
    path('test/', views.chat_test, name="chat_test"),
    
    path("testview/", test.test, name='ttttt'),


    #동행모집글 By 수현
    path('community/', views.community, name='community'),

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

