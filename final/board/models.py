from django.db import models
from trip.models import User
# Create your models here.
class Post(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
    review = models.PositiveBigIntegerField(verbose_name='조회수', default=0)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')
    top_fixed = models.BooleanField(verbose_name='상단고정', default=False)

    def __str__(self):
        return self.title

    class Meta:
        db_table = '게시판'
        verbose_name = '게시판'