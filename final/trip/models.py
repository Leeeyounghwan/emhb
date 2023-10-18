from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
# Create your models here.

def upload_to(instance, filename):
    today = datetime.now()
    table_name = instance._meta.db_table  # 테이블명 가져오기
    return 'images/{0}/{1}/{2}/{3}'.format(table_name, today.year, today.month, today.day, filename)

class User(AbstractUser):
    nickname = models.CharField(max_length=40)
    profile_image = models.ImageField(upload_to=upload_to, null=True)
    review = models.IntegerField(default=0)
    number_of_written = models.IntegerField(default=0)
    is_black = models.BooleanField(default=False)
    
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
    post_image = models.ImageField(upload_to=upload_to, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    region = models.CharField(max_length=20)
    recuited_people =models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

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
    image = models.ImageField(upload_to=upload_to, null=True)
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
    
    