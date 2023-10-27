from django.contrib import admin

# Register your models here.
from .models import Post

class NoticeAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'writer', 
        'review',
        'create_at',
        )
    search_fields = ('title', 'content', 'writer__user_id',)

admin.site.register(Post, NoticeAdmin)