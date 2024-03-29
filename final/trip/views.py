from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
# from .forms import CommentForm

from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from .models import Package, User, Report,Schedule,ScheduleComment, Community, TogetherPost,TogetherComment, GroupChat, WishList
from django.contrib.auth.decorators import login_required
import openai
from django.http import JsonResponse
import json
from django.contrib import messages
from .forms import UserForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from .forms import UserProfileForm, CommentForm
from django.contrib.auth import update_session_auth_hash
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage

from .serializer import GroupChatSerializer
# Create your views here.

# 메인페이지 시작 By 영환

def search_trip(request):

    if request.method == "POST":
        action = request.POST.get('action')
        if action == 'search':
            search_region = request.POST['region']
            posts = TogetherPost.objects.filter(region=search_region)
        context = {
            "search_region" : search_region,
            "posts" : posts
        }
    return render(request, 'together_walk.html',context)

# 메인페이지 종료

# 마이페이지 시작 By 영환
@login_required
def profile(request): #내 정보 수정
    user = request.user
    form = UserProfileForm(initial={'username': user.username})
    user_info = get_object_or_404(User, username=user.username)
    print(user_info.profile_image)

    if request.method == 'POST' and user_info.profile_image == "":
        user_info.profile_image = request.FILES['profile_img']
        user_info.save()
        return redirect('trip:profile')
    
    if request.method == 'POST' and user_info.profile_image != "":
        form = UserProfileForm(request.POST)
        if 'profile_img' in request.FILES:
            user_info.profile_image = request.FILES['profile_img']
            user_info.save()

            context = {
                "form" : form,
                "user_info" : user_info
            }
            return redirect('trip:profile')

        if form.is_valid():
            nickname = form.cleaned_data['nickname']
            password = form.cleaned_data['password']
            password_confirm = form.cleaned_data['password_confirm']

            if nickname != user.nickname:
                user.nickname = nickname
                user.save()
                messages.success(request, '닉네임이 업데이트되었습니다.')

            if password:
                if password == password_confirm:
                    
                    user.set_password(password)
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, '비밀번호가 업데이트되었습니다.')
                else:
                    messages.error(request, '비밀번호와 비밀번호 확인이 일치하지 않습니다.')
            context = {
                "form" : form,
                "user_info" : user_info
            }
            return redirect('trip:profile')

    context = {
        "form" : form,
        "user_info" : user_info
    }

    return render(request, 'mypage/profile.html', context)

@login_required
def mytopics(request):#내가 쓴 글 보기
    
    login_username = request.user.username
    login_user = get_object_or_404(User, username=login_username)

    my_posts = TogetherPost.objects.filter(user_id_id=login_user.id)

    context = {
        "my_posts" : my_posts
    }

    return render(request, 'mypage/mytopics.html', context)

@login_required
def myfeadback(request): #내가받은 후기 보기
    return render(request,'mypage/myfeadback.html')

@login_required
def like_schedule(request): #찜한 일정 리스트
    user_id   = request.user.id
    wish_list = WishList.objects.filter(user_id_id=user_id)
    package_list = []

    for i in range(0, len(wish_list)):
        package = get_object_or_404(Package, id=wish_list[i].product_id)
        package_list.append(package)
    
    context = {
        'items' : package_list
    }
    return render(request,'mypage/like_schedule.html', context)
    # return render(request,'mypage/like_test.html')


@login_required
def add_wishlist(request,id): # 위시리스트 추가
    user_id = request.user.id

    if not WishList.objects.filter(user_id_id = user_id, product_id = id).exists():
        add_wishlist = WishList(user_id_id = user_id,product_id = id,created_at = timezone.now())
        add_wishlist.save()

        # wish_list = WishList.objects.filter(user_id_id=user_id)
        # package_list = []

        # for i in range(0, len(wish_list)):
        #     package = get_object_or_404(Package, id=wish_list[i].product_id)
        #     package_list.append(package)
        
        # context = {
        #     'package' : package_list
        # }
    
    else:
        WishList.objects.get(user_id_id = user_id, product_id = id).delete()
        return redirect("trip:package_detail", id)
    return redirect("trip:package_detail", id)
    # return render (request, "mypage/like_schedule.html",context)


@login_required
def chatting_room(request): #채팅방리스트
    return render(request,'mypage/chatting_room.html')

@login_required
def user_report(request):
    return render(request, 'mypage/user_report.html')

@login_required
def report_submit(request):
    report = Report()
    if request.method == "POST":
        report.user_id_id = request.user.id
        report.reported_user = request.POST['reported_user']
        report.report_reason = request.POST['report_content']
        report.save()

    return redirect('trip:view_report')

@login_required
def view_report(request):
    report_list = Report.objects.filter(user_id_id=request.user.id, is_deleted=False)
    context = {
        "report_list" : report_list
    }
    return render(request, "mypage/view_report.html", context)

@login_required
def view_user_report(request, id) :
    report_detail = get_object_or_404(Report, id=id)
    context = {
        "report_detail" : report_detail
    }
    return render(request, "mypage/view_user_report.html", context)

@login_required
def report_update(request, id):
    report = get_object_or_404(Report, id=id)
    if request.method == "POST":
        action = request.POST.get('action')
        if action == 'update':
            report.report_reason = request.POST['report_content']
            print(report.report_reason)
            report.save()

        elif action == 'delete':
            report.is_deleted = True
            report.save()

    return redirect('trip:view_report')

# 마이페이지 종료

def post_detail(request, post_id):
    return render(request, 'post_detail.html')

# 관리자페이지 시작 by 영환

@login_required
def admin_check(request):
    if request.user.is_authenticated:
        user = request.user.username
        user_info = get_object_or_404(User, username=user)
        if user_info.is_staff == True :
            return True
        else:
            return False
        
@login_required
def admin_page(request):

    if admin_check(request) == True :
        return render(request,"admin/admin_page.html")
    else:
        return render(request, "index.html")

def admin_management(request):

    if admin_check(request) == True :
        user_list = User.objects.all().order_by('-is_staff')
        context = {
            'user_list' : user_list
        }

        return render(request, "admin/admin_management.html", context)
    else:
        return render(request, "index.html")

@login_required
def change_state(request, username):
    
    if admin_check(request) == True :
        if request.method == "POST":
            user = get_object_or_404(User, username=username)
            action = request.POST.get('action')
        if action == 'to_user':
            user.is_staff = False
            user.save()
        elif action == 'to_admin':
            user.is_staff = True
            user.save()

        user_list = User.objects.all().order_by('-is_staff')
        context = {
            'user_list' : user_list
        }
        return render(request, "admin/admin_management.html", context)
    else:
        return render(request, "main.html")

@login_required 
def create_product(request):

    if admin_check(request) == True :
        package = Package()
        if request.method == "POST":
            package.title = request.POST['title']
            package.price = request.POST['price']
            package.destination = request.POST['destination']
            package.start_date = request.POST['start_date']
            package.end_date = request.POST['end_date']
            package.content = request.POST['content']
            package.post_author_id = request.user.id
            if 'package_image' in request.FILES:
                package.image = request.FILES['package_image']
            package.save()
            return redirect('trip:product_management')

        return render(request, "admin/create_product.html")
    else :
        return redirect("trip:main")

@login_required
def update_product(request, package_id):

    if admin_check(request) == True :
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
        return render(request, "admin/update_product.html", context)
    else:
        return redirect("trip:main")

@login_required
def product_management(request):

    if admin_check(request) == True :
        packages = Package.objects.filter(is_deleted=False).order_by('id')
        context = {
            "packages" : packages
        }
        return render(request, "admin/product_management.html", context)

    else:
        return redirect("trip:main")    

@login_required
def deleted_product(request):
    if admin_check(request) == True :
        deleted_packages = Package.objects.filter(is_deleted=True).order_by('-updated_at')
        context = {
            "deleted_packages" : deleted_packages
        }
        return render(request, "admin/deleted_product.html", context)
    else:
        return redirect("trip:main")

@login_required
def delete_cancel(request, package_id):

    if admin_check(request) == True :
        package = get_object_or_404(Package, id=package_id)
        package.is_deleted = False
        package.save()

        return redirect("trip:product_management")
    else:
        return redirect("trip:main")

@login_required
def order_inquiry(request):
    if admin_check(request) == True :
        return render(request, "admin/order_inquiry.html")
    else:
        return redirect("trip:main")

@login_required
def delivery_tracking(request):
    if admin_check(request) == True :
        return render(request, "admin/delivery_tracking.html")
    else:
        return redirect("trip:main")
    
@login_required
def return_management(request):
    if admin_check(request) == True :
        return render(request, "admin/return_management.html")
    else:
        return redirect("trip:main")

@login_required
def report_detail(request):

    if admin_check(request) == True :
        reports = Report.objects.all().filter(is_deleted=False).order_by('is_completed', 'created_at', 'updated_at')
        
        context = {
            "reports" : reports
        }
        return render(request, "admin/report_detail.html", context)
    else:
        return redirect("trip:main")

@login_required
def view_report_detail(request, id):

    if admin_check(request) == True :
        report_detail = Report.objects.filter(id=id)
        print(report_detail[0].user_id_id)
        # 신고한 유저 정보
        user_info = get_object_or_404(User, id=report_detail[0].user_id_id)
        # 신고당한 유저 정보
        reported_user_info = get_object_or_404(User, nickname=report_detail[0].reported_user)
        print(reported_user_info.username)
        context = {
            "report_detail" : report_detail[0],
            "user_info" : user_info,
            "reported_user_info" : reported_user_info
        }
        return render(request, "admin/view_report_detail.html", context)
    else:
        return redirect("trip:main")

@login_required
def report_complete(request, id):

    if admin_check(request) == True :
        report = get_object_or_404(Report, id=id)
        reported_user_info = get_object_or_404(User, nickname=report.reported_user)

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
    else:
        return redirect("trip:main")

@login_required
def blacklist_management(request):

    if admin_check(request) == True :
        blacklists = User.objects.filter(is_black=True)
        context = {
            "blacklists" : blacklists
        }
        return render(request, "admin/blacklist_management.html", context)
    else:
        return redirect("trip:main")

@login_required
def black_cancel(request, blacklist_id):

    if admin_check(request) == True :
        blacklist = get_object_or_404(User, id=blacklist_id)
        print(blacklist.is_black)

        blacklist.is_black = False
        blacklist.save()

        return redirect("trip:blacklist_management")
    else:
        return redirect("trip:main") 

# 관리자페이지 종료


#by 건영
def index(request):
    together_walk = TogetherPost.objects.all().order_by('created_at')
    packages = Package.objects.all().order_by('-created_at')

    together_list = []
    package_list = []

    for i in range(0, 8) :
        together_list.append(together_walk[i])
    for j in range(0, 6) :
        package_list.append(packages[j])

    context = {
        "posts" : together_list,
        "packages" : package_list
    }

    return render(request, 'index.html', context)
def about(request):
    return render(request, 'about.html')

def together_walk(request):
    posts = TogetherPost.objects.all()


    posts_per_page = 6

    page_number = request.GET.get('page')
    try:
        page_number = int(page_number)
    except (ValueError, TypeError):
        page_number = 1 

    paginator = Paginator(posts, posts_per_page)

    try:
        current_page = paginator.page(page_number)
    except EmptyPage:
        current_page = paginator.page(1)

    return render(request, 'together_walk.html', {'posts': current_page})

def contact(request):
    return render(request, 'contact.html')
def elements(request):
    return render(request, 'elements.html')
def main(request):
    return render(request, 'main.html')
@login_required
def together_detail(request, id):
    try:
        post = TogetherPost.objects.get(id=id)
        comments = TogetherComment.objects.filter(post_id_id=post.id)
        post_writer = get_object_or_404(User, id=post.user_id_id)

    except TogetherPost.DoesNotExist:
        raise Http404("포스트를 찾을 수 없습니다.")
    
    if request.method == "POST":
        comment_id = request.POST.get("comment_id")
        try:
            comment = TogetherComment.objects.get(id=comment_id)
            comment.delete()  # 댓글 삭제
        except TogetherComment.DoesNotExist:
            pass  # 댓글이 이미 삭제된 경우 무시
        
        post = TogetherPost.objects.get(id=id)
    context = {
        "post": post,
        'username':request.user,
        "comments" : comments,
        "post_writer" : post_writer
    }
    return render(request, 'together_detail.html', context)

@login_required
def add_comment(request, id):
    post = get_object_or_404(TogetherPost, id=id)
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post_id = post 
            comment.content_writer_id = request.user.id
            comment.writer_nickname = request.user.nickname
            comment.save()
            return redirect('trip:together_detail', id=post.id)
    
    return redirect('trip:together_detail', id=post.id)

@login_required
def delete_comment(request, id):
    comment = TogetherComment.objects.get(id=id)
    comment.delete()
    return redirect('trip:together_detail', id=comment.post_id.id)

#by 건영 종료

# 로그인, 회원가입 페이지 by 문정


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(request, request.POST)
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        # user = authenticate(request, username=username, password=password)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                is_admin = get_object_or_404(User, username=username)
                if is_admin.is_staff:
                    # return render(request, 'admin/admin_page.html')
                    return redirect('trip:admin_page')
                else:
                    return redirect('trip:index')
            else:
                return render(request, 'login.html', {'form': form, 'error': '아이디 또는 비밀번호가 틀렸습니다.'})
        else:
            print("error")
            print(form.errors)
    form = UserLoginForm()

    #     else:
    #         return render(request,'login.html', {'error':'username or password is incorrect'})
    # else:
    return render(request,'login.html', {"form":form})
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
    return redirect('trip:index')

def register(request):
    # return render(request, 'register.html')
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            print(form)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('trip:index')
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
            "content": "너는 우리 트립웹에 Trip봇이야. 답변은 200자 내로 .으로완결지어 "},
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
  items =  Package.objects.filter(is_deleted=False)
  context = {
      'items' : items
  }
  return render(request, 'packages.html', context)

@login_required
def package_detail(request, id):
    package = get_object_or_404(Package, id=id)

    post_author = get_object_or_404(User, id=package.post_author_id)
    user_id = request.user.id
    check_wish = True # 위시리스트에 있으면 

    if not WishList.objects.filter(product_id = id, user_id_id = user_id):
        check_wish = False
    context = {
        "check_wish" : check_wish,
        "package" : package,
        "post_author" : post_author 
    }
    return render(request, 'package_detail.html', context)



# 실시간 채팅 뷰
def chatting(request):
    return render(request, 'chat/index.html')

@login_required
def room(request, room_name):
    chat_rooms = GroupChat.objects.filter(room_name=room_name)
    if request.method == "GET":
        if chat_rooms.exists():
            chat_room = chat_rooms.first()
            chat_room.members.add(request.user)
            return render(request, 'chat/room.html', {"room_name": room_name,"username":request.user})
        else:
            chat_room = GroupChat.objects.create()
            chat_room.members.add(request.user)
            return render(request, 'chat/room.html', {"room_name": chat_room.room_name,
                                                      "username": request.user})
        
    return redirect("trip:main")

@login_required
def check_room(request, room_name, room_title):
    chat_room , is_created = GroupChat.objects.get_or_create(room_name=room_name)
    chat_room.members.add(request.user)
    if is_created:
        chat_room.room_title = room_title
        chat_room.save()
        
    return JsonResponse({'is_ok':is_created})
    
@login_required
def room_list(request):
    chat_list = GroupChat.objects.filter(members=request.user).order_by('-created_at')
    serializer = GroupChatSerializer(chat_list, many=True)
    data = serializer.data
    return JsonResponse(data, safe=False)

@login_required
def chat_test(request):
    chat_room_list = GroupChat.objects.filter(members=request.user)
    context = {
        'username':request.user,
        'chat_room_list':chat_room_list
    }
    return render(request, 'chat/chat_merge.html', context)

@login_required
def community(request):
    posts = TogetherPost.objects.all()

    posts_per_page = 6

    page_number = request.GET.get('page')
    try:
        page_number = int(page_number)
    except (ValueError, TypeError):
        page_number = 1 

    paginator = Paginator(posts, posts_per_page)

    try:
        current_page = paginator.page(page_number)
    except EmptyPage:
        current_page = paginator.page(1)

    return render(request, 'community.html', {'posts': current_page})

@login_required
def community_write(request):
    return render(request, 'community_write.html')

# def set_write(request):

@login_required
def set_region(request):
  if 'region-button' in request.POST:
    region = request.POST.get('region-setting')
    area = {"region": region}
    
    # 확인용(region)
    print(region)
    
    return render(request, 'community_write.html', area)

  
def set_write(request):
    if 'set_write_button' in request.POST:
        Together_post = TogetherPost.objects.create(
            post_title = request.POST['title'],
            post_content = request.POST['messages'],
            start_date = request.POST['start_date'],
            end_date = request.POST['end_date'],
            
            # Lnt, Lat 값 
            post_lnt = request.POST['lng'],
            post_lat = request.POST['lat'],

            region = request.POST['community_destination'],
            recuited_people = request.POST['recruitment'],
            user_id = request.user,
        )

        print(Together_post)

        Together_post.save()
        return redirect('trip:community')
    else:
        return render(request, 'community_write.html')


def delete_write(request, id):
    together_post = get_object_or_404(TogetherPost, id=id)
    together_post.delete()
    return redirect('trip:blog')
