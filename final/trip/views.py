from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . import forms
from .models import User

# Create your views here.

def main(request):
    return render(request, 'index.html')

def user_login(request):
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('trip:main')

def register(request):
    # error_message = ''
    # if request.method == 'POST':
    #     form = forms.UserForm(request.POST)
    #     username = request.POST.get('username')
    #     nickname = request.POST.get('nickname')
    #     if User.objects.filter(username=username).exists():
    #         error_message = "이미 존재하는 아이디입니다."
    #     elif form.is_valid():
            
    #         password1 = form.cleaned_data['password1']
    #         password2 = form.cleaned_data['password2']
            
    #         # 비밀번호 일치 여부를 확인
    #         if password1 == password2:
    #             # 새로운 유저를 생성
    #             user = User.objects.create_user(username=username, password=password1, nickname = nickname)
                
    #             # 유저를 로그인 상태로 만듦
    #             # login(request, user)
            
            
    #             return redirect('trip:login')
    #         else:
    #             form.add_error('password2', 'Passwords do not match')
    # else:
    #     form = forms.RegistrationForm()
    # return render(request, 'register2.html' , {'error_message': error_message})
    return render(request, 'register.html')
