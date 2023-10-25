# Register your models here.
from django.contrib import admin
from .models import User, TogetherPost, TogetherComment, Schedule,ScheduleComment, TravelDestination, ChoicePost, Voucher, Package, Community

admin.site.register(User)
admin.site.register(TogetherPost)
admin.site.register(TogetherComment)
admin.site.register(Schedule)
admin.site.register(ScheduleComment)
admin.site.register(TravelDestination)
admin.site.register(ChoicePost)
admin.site.register(Voucher)
admin.site.register(Package)
admin.site.register(Community)