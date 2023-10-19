from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse

# Create your views here.

#마이페이지 by 준경
def mypage(request):
    return render(request, 'mypage.html')


# 관리자페이지 시작 by 영환
def main(request):
    return render(request, "main.html")

def admin_page(request):
    return render(request, "admin/admin_page.html")

def create_product(request):
    return render(request, "admin/create_product.html")

def product_management(request):
    return render(request, "admin/product_management.html")

def deleted_product(request):
    return render(request, "admin/deleted_product.html")
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
    return render(request, 'single-blog.html')

def comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            messages.success(request, '댓글이 성공적으로 작성되었습니다.')
            return redirect('comment_list')
    else:
        form = CommentForm()

    return render(request, 'single-blog.html', {'form': form})

#by 건영 종료

# 로그인, 회원가입 페이지 by 문정
def user_login(request):
    # if request.method == 'POST':
    #     form = AuthenticationForm(request=request, data=request.POST)
    #     if form.is_valid():
    #         login(request, form.get_user())
    #         return redirect('trip:main')  # 로그인 성공 시 리디렉션할 페이지
    # else:
    #     form = AuthenticationForm()
    # return render(request, 'login.html', {'form': form})
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request,'main.html')
    #     else:
    #         return render(request,'login.html', {'error':'username or password is incorrect'})
    # else:
    return render(request,'login.html')



def user_logout(request):
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