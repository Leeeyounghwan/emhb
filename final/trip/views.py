from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from .models import TogetherPost,TogetherComment

# from .forms import CommentForm

from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from .models import Package, User, Report,Schedule,ScheduleComment
from django.contrib.auth.decorators import login_required
import openai
from django.http import JsonResponse
import json
from django.contrib import messages
from .forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from .forms import UserProfileForm
from django.contrib.auth import update_session_auth_hash

# Create your views here.

#마이페이지 by 준경

#@login_required
def profile(request): #내 정보 수정
    user = request.user
    form = UserProfileForm(initial={'username': user.username})

    if request.method == 'POST':
        form = UserProfileForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            password_confirm = form.cleaned_data['password_confirm']

            if username != user.username:
                user.username = username
                user.save()
                messages.success(request, '아이디가 업데이트되었습니다.')

            if password:
                if password == password_confirm:
                    user.set_password(password)
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, '비밀번호가 업데이트되었습니다.')
                else:
                    messages.error(request, '비밀번호와 비밀번호 확인이 일치하지 않습니다.')

            return redirect('profile')

    return render(request, 'mypage/profile.html', {'form': form})

def mytopics(request):#내가 쓴 글 보기
  return render(request, 'mypage/mytopics.html', {'posts' : TogetherPost.objects.all()})

def myfeadback(request): #내가받은 후기 보기
    return render(request,'mypage/myfeadback.html')

def like_schedule(request): #찜한 일정 리스트
    return render(request,'mypage/like_schedule.html',{'schedules' : Schedule.objects.all()})

def chatting_room(request): #채팅방리스트
    return render(request,'mypage/chatting_room.html')



# 관리자페이지 시작 by 영환
def main(request):
    return render(request, "main.html")

def admin_check(request):
    if request.user.is_authenticated:
        user = request.user.username
        user_info = get_object_or_404(User, username=user)
        if user_info.is_staff == True :
            return True
        else:
            return False

def admin_page(request):

    # if admin_check(request) == True :
    #     return redirect("trip:admin_page")
    # else:
        return render(request, "admin/admin_page.html")


def create_product(request):

    package = Package()
    if request.method == "POST":
        package.title = request.POST['title']
        package.price = request.POST['price']
        package.destination = request.POST['destination']
        package.start_date = request.POST['start_date']
        package.end_date = request.POST['end_date']
        package.content = request.POST['content']
        if 'package_image' in request.FILES:
            package.image = request.FILES['package_image']
        package.save()
        return redirect('trip:product_management')
    
    # if admin_check(request) == True :
    return render(request, "admin/create_product.html")
    # else:
    #     return redirect("trip:main")

def update_product(request, package_id):

    package = get_object_or_404(Package, id=package_id)
    if package:
        package.content = package.content.strip()
    
    if request.method == "POST":
        action = request.POST.get('action')
        if action == 'update':
            package.title = request.POST['title']
            package.price = request.POST['price']
            package.destination = request.POST['destination']
            package.start_date = request.POST['start_date']
            package.end_date = request.POST['end_date']
            package.content = request.POST['content']
            if 'package_image' in request.FILES:
                package.image = request.FILES['package_image']
            package.save()
            return redirect('trip:product_management')
        
        elif action == 'delete':
            package.is_deleted = True
            package.save()
            return redirect('trip:product_management')

    context = {
        'package' : package
    }

    # if admin_check(request) == True :
    return render(request, "admin/update_product.html", context)
    # else:
    #     return redirect("trip:main")


def product_management(request):

    packages = Package.objects.filter(is_deleted=False).order_by('id')
    context = {
        "packages" : packages
    }
    return render(request, "admin/product_management.html", context)

    # if admin_check(request) == True :
    #     packages = Package.objects.all()
    #     context = {
    #         "packages" : packages
    #     }

    #     return render(request, "admin/product_management.html", context)
    # else:
    #     return redirect("trip:main")    

def deleted_product(request):

    deleted_packages = Package.objects.filter(is_deleted=True).order_by('-updated_at')
    context = {
        "deleted_packages" : deleted_packages
    }
    return render(request, "admin/deleted_product.html", context)

    # if admin_check(request) == True :
    #     deleted_packages = Package.objects.filter(is_deleted=True).order_by('-updated_at')
    #     context = {
    #         "deleted_packages" : deleted_packages
    #     }

    #     return render(request, "admin/deleted_product.html", context)
    # else:
    #     return redirect("trip:main")

def delete_cancel(package_id):

    package = get_object_or_404(Package, id=package_id)
    print(package.is_deleted)

    package.is_deleted = False
    package.save()
    print(package.is_deleted)

    return redirect("trip:product_management")

def order_inquiry(request):
    return render(request, "admin/order_inquiry.html")

def delivery_tracking(request):
    return render(request, "admin/delivery_tracking.html")

def return_management(request):
    return render(request, "admin/return_management.html")

def report_detail(request):

    reports = Report.objects.all().order_by('is_completed', 'created_at', 'updated_at')
    
    context = {
        "reports" : reports
    }

    return render(request, "admin/report_detail.html", context)

    # if admin_check(request) == True :
    #     reports = Report.objects.all()
    #     context = {
    #         "reports" : reports
    #     }

    #     return render(request, "admin/report_detail.html", context)
    # else:
    #     return redirect("trip:main")

def view_report_detail(request, id):
    report_detail = Report.objects.filter(id=id)
    # 신고한 유저 정보
    user_info = get_object_or_404(User, id=report_detail[0].user_id_id)
    # 신고당한 유저 정보
    reported_user_info = get_object_or_404(User, username=report_detail[0].reported_user)
    context = {
        "report_detail" : report_detail[0],
        "user_info" : user_info,
        "reported_user_info" : reported_user_info
    }
    return render(request, "admin/view_report_detail.html", context)

def report_complete(request, id):
    report = get_object_or_404(Report, id=id)
    reported_user_info = get_object_or_404(User, username=report.reported_user)

    if request.method == "POST":
        action = request.POST.get('action')
        if action == 'commit':
            report.report_reply = request.POST['reply']
            report.is_completed = True
            report.completed_at = timezone.now()
            report.save()
        
        elif action == 'count_up':
            report.report_reply = request.POST['reply']
            report.is_completed = True
            report.completed_at = timezone.now()
            report.save()
            if reported_user_info.caution_cnt >= 9 :
                reported_user_info.is_black = True
            else:
                reported_user_info.caution_cnt += 1
            reported_user_info.save()
        
        elif action == 'update':
            report.report_reply = request.POST['reply']
            report.updated_at = timezone.now()
            report.save()

        elif action == 'delete':
            report.report_reply = ""
            report.is_completed = False
            report.updated_at = timezone.now()
            report.save()

    reports = Report.objects.all().order_by('is_completed', 'created_at', 'updated_at')
    
    context = {
        "reports" : reports
    }
    return render(request, "admin/report_detail.html", context)


def blacklist_management(request):

    blacklists = User.objects.filter(is_black=True)
    context = {
        "blacklists" : blacklists
    }
    return render(request, "admin/blacklist_management.html", context)
    # if admin_check(request) == True :
    #     blacklist = User.objects.filter(is_black=True)
    #     context = {
    #         "blacklist" : blacklist
    #     }

    #     return render(request, "admin/blacklist_management.html", context)
    # else:
    #     return redirect("trip:main")

def black_cancel(request, blacklist_id):
    # print(blacklist_id)
    blacklist = get_object_or_404(User, id=blacklist_id)
    print(blacklist.is_black)

    blacklist.is_black = False
    blacklist.save()

    return redirect("trip:blacklist_management")

# 관리자페이지 종료


#by 건영
def index(request):
    return render(request, 'index.html')
def about(request):
    return render(request, 'about.html')
def blog(request):
    return render(request, 'blog.html')
def contact(request):
    return render(request, 'contact.html')
def elements(request):
    return render(request, 'elements.html')
def main(request):
    return render(request, 'main.html')
def packages(request):
    return render(request, 'packages.html')
def single_blog(request):
    post = get_object_or_404(TogetherPost)
    return render(request, 'single-blog.html',{'post':post})
@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        user = request.user
        content = request.POST['content']
        comment = TogetherComment(post_id_id=post_id, content=content)
        comment.save()
        return redirect('single-blog.html', post_id=post_id)
    return redirect('single-blog.html')

#by 건영 종료

# 로그인, 회원가입 페이지 by 문정

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('trip:main')
            return render(request,'register.html')
    #     else:
    #         return render(request,'login.html', {'error':'username or password is incorrect'})
    # else:
    return render(request,'login.html')
    # if request.method == 'POST':
    #     form = UserCreationForm(request.form)
    #     if form.is_valid():
    #         user = form.save()
    #         login(request, user)
    #         return redirect('trip:main')
    # else:
    #     form = UserCreationForm()
    # return render(request,'login.html') 



def user_logout(request):
    logout(request)
    redirect('trip:main')

def register(request):
    # return render(request, 'register.html')
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('trip:main')
    else:
        form = UserForm()
    return render(request, 'register.html', {'form': form})


# 챗봇 BY 영민
def chatapi(request, question):
    with open('trip/config.json', 'r') as f:
        json_data = json.load(f)
    api_key = json_data['OPENAI_KEY']
                
    response_generator = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {
            "role": "system",
            "content": "너는 우리 트립웹에 Trip봇이야. 답변은 400자 내로 깔끔하게"},
            {"role": "user", "content": f"'{question}'"},
        ],
        temperature=0.5,
        max_tokens=400,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        api_key=api_key,
    )
    content = response_generator['choices'][0]['message']['content']
    answer = {'answer':content}
    return JsonResponse(answer)

def chatbot(request):
    return render(request, 'test.html')
def packages(request):
  return render(request, 'packages.html', {'items' : Package.objects.all()})

def chatting(request):
    return render(request, 'chat/index.html')

def room(request, room_name):
    return render(request, 'chat/room.html', {"room_name": room_name})

def community(request):
    render(request, 'community.html')