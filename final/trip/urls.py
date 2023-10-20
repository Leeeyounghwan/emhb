from django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static

app_name = 'trip'
urlpatterns = [
    path('mypage', views.mypage, name='mypage'),#마이페이지 url by 준경
    path('charts/', views.charts, name='charts'),
    
    
    # 관리자 페이지 관련 urlpatterns by 영환
    path("admin_page/", views.admin_page, name="admin_page"),
    path("admin_page/create_product", views.create_product, name="create_product"),
    path("admin_page/product_management", views.product_management, name="product_management"),
    path("admin_page/deleted_product", views.deleted_product, name="deleted_product"),
    path("admin_page/order_inquiry", views.order_inquiry, name="order_inquiry"),
    path("admin_page/delivery_tracking", views.delivery_tracking, name="delivery_tracking"),
    path("admin_page/return_management", views.return_management, name="return_management"),
    path("admin_page/report_detail", views.report_detail, name="report_detail"),
    path("admin_page/user_management", views.user_management, name="user_management"),
    path("admin_page/blacklist_management", views.blacklist_management, name="blacklist_management"),
    # 관리자 페이지 관련 urlpatterns 종료

    #by 건영
    path('',views.index, name = "index"),
    path('about/',views.about, name='about'),
    path('blog/',views.blog, name='blog'),
    path('contact/',views.contact, name='contact'),
    path('elements/',views.elements, name='elements'),
    path('main/',views.main, name='main'),
    
    path('packages/',views.packages, name='packages'),
    
    # path('single_blog/1/',views.single_blog, name='single_blog'), 
    # path('single_blog/<int:post_id>/',views.single_blog, name='single_blog'), 
    
    # path('post/<int:post_id>/together_comment/', views.together_comment,  name='together_comment'),  #댓글
    
    path('single_blog/',views.single_blog, name='single_blog'),
    # path('comment/', views.comment,  name='comment'),  #댓글

    # 로그인, 회원가입 페이지 by 문정
    path('login/', views.user_login, name = 'login'),
    path('logout/', views.user_logout, name= 'logout'),
    path('register/', views.register, name='register'),
    
    #CHATBOT BY 영민
    path('chatbot/', views.chatbot, name='chatbot'),
    path('chatapi/<str:question>', views.chatapi, name='chatapi'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

