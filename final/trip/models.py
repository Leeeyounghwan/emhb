from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import datetime
# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(max_length=40, blank=True)
    profile_image = models.ImageField(upload_to="", null=True)
    review = models.IntegerField(default=0)
    number_of_written = models.IntegerField(default=0)
    is_black = models.BooleanField(default=False)
    caution_cnt = models.IntegerField(default=0)
    
    # 경고 횟수 관련 내용 추가 - 2023.10.23 by 영환
    caution_cnt = models.IntegerField(default=0)
    
    # AbstractUser 기본 필드
    # username_validator = UnicodeUsernameValidator()
    # username = models.CharField(_('username'), max_length=150, unique=True,…)
    # first_name = models.CharField(_('first name'), max_length=30, blank=True)
    # last_name = models.CharField(_('last name'), max_length=150, blank=True)
    # email = models.EmailField(_('email address'), blank=True)
    # is_staff = models.BooleanField(_('staff status'), default=False,…)
    # is_active = models.BooleanField(_('active'), default=True,…)
    # date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    
    
class TogetherPost(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=40)
    post_content = models.TextField()
    
    # Lnt, Lat 값을 가져오기로 함(주석처리)
    # post_image = models.ImageField(upload_to="TogetherPost_images/", null=True, blank=True)
    
    start_date = models.DateField()
    end_date = models.DateField()
    region = models.CharField(max_length=20)
    recuited_people =models.CharField(max_length=5)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    # # 이미지 업로드를 위한 칼럼 추가 BY수현
    # post_lnt = models.CharField(max_length=50)
    # post_lat = models.CharField(max_length=50)
    

class TogetherComment(models.Model):
    post_id = models.ForeignKey(TogetherPost, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    
class Schedule(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    dest_code = models.IntegerField()
    recuited_people =models.CharField(max_length=5)
    start_date = models.DateField()
    end_date = models.DateField()
    image = models.ImageField(upload_to="", null=True)
    detail = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    
class ScheduleComment(models.Model):
    post_id = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

class TravelDestination(models.Model):
    post_id = models.OneToOneField(Schedule, on_delete=models.CASCADE, related_name='destination')
    travel_name = models.CharField(max_length=20)
    continent = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    region = models.CharField(max_length=20)
    
class ChoicePost(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    together_post = models.ForeignKey(TogetherPost, on_delete=models.CASCADE, null=True)
    shedule_post = models.ForeignKey(Schedule, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    
class Voucher(models.Model):
    buyer_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    dest_code = models.ForeignKey(TravelDestination, on_delete=models.CASCADE)
    accommodation = models.CharField(max_length=30)
    description = models.TextField(null=True)
    review = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    is_sold = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    
# packages.html에 사용할 추가 모델 2023-10-18 by 수현
class Package(models.Model):
    destination = models.CharField(max_length=40)
    title = models.CharField(max_length=200)
    price = models.IntegerField()
    image = models.ImageField(upload_to='package_images/', null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_date = models.DateField()
    end_date = models.DateField()
    # 삭제관련 컬럼 추가 - 2023.10.19 by 영환
    is_deleted = models.BooleanField(default=False)

# 신고 관련 모델 추가 - 2023.10.19 by 영환
# default관련 옵션 변경 - 2023.10.23 by 영환
class Report(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    reported_user = models.CharField(max_length=40)
    report_reason = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_completed = models.BooleanField(default=False, null=True)
    completed_at = models.DateTimeField(auto_now=False, null=True)
    is_deleted = models.BooleanField(default=False)
    report_reply = models.TextField(null=False, default="")

#받은후기 관련 모델 추가 - 2023.10.22 by 준경
# class Feedback(models.Model):
#     receiver_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     sender_id = 

    
class GroupChat(models.Model):
    room_name = models.AutoField(primary_key=True)
    room_title = models.CharField(max_length=200, null=True, default='test')
    members = models.ManyToManyField(User, related_name='group_chat_rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    last_message = models.TextField(null=True, blank=True)
    last_message_sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='last_message_sender')

    def __str__(self):
        return self.room_title

def user_profile_upload_path(instance, filename):
    # 현재 날짜를 기반으로 디렉토리 경로 생성
    today = datetime.today()
    return f"message/userprofile/{today.year}/{today.month}/{today.day}/{filename}"

class Message(models.Model):
    group_chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE, related_name="chat_messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user_profile = models.ImageField(null=True, upload_to=user_profile_upload_path)

# 동행모집글 관련 모델 추가 2023-10-23 by 수현
class Community(models.Model):
    nickname = models.ForeignKey(User, on_delete=models.CASCADE)
    # profileImage = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='community_images/', null=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    recruitment = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    community_destination = models.CharField(max_length=200, null=True, blank=True)
    
class WishList(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    product = models.ForeignKey(Package, on_delete=models.CASCADE, null=False, default="" )
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)