from django import forms
from .models import Package
from django.contrib.auth.forms import UserCreationForm
from . models import User


class Package(forms.ModelForm):
  class Meta:
    model = Package
    exclude = ['created_at','updated_at']
    fields = ['destination', 'title', 'price', 'image', 'content', 'start_date', 'end_date', 'created_at', 'updated_at']

class UserForm(UserCreationForm):
    nickname = forms.CharField(max_length=40, required=False)

    class Meta:
        model = User
        fields= ['username', 'password1', 'password2', 'nickname']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['username'].widget.attrs['id'] = 'username'
        self.fields['password1'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['password1'].widget.attrs['id'] = 'password1'
        self.fields['password2'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['password2'].widget.attrs['id'] = 'password2'
        self.fields['nickname'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['nickname'].widget.attrs['id'] = 'nickname'


class UserLoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields= ['username', 'password']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['username'].widget.attrs['id'] = 'username'
        self.fields['password'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['password'].widget.attrs['id'] = 'password'
# class UserModelForm(forms.ModelForm):
    
#     class Meta:
#         model = User
#         fields = ['username', 'password', 'nickname']
        
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['username'].widget.attrs['class'] = 'form-control form-control-user'
#         self.fields['username'].widget.attrs['id'] = 'username'

#마이페이지 정보수정form by 준경
class UserProfileForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': '아이디를 입력해주세요', 'class': 'login-input'}),
        label='아이디',
        label_suffix='',
        required=True
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '새로운 비밀번호를 입력해주세요', 'class': 'login-input'}),
        label='새로운 비밀번호',
        label_suffix='',
        required=False
    )

    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '새로운 비밀번호를 다시 입력해주세요', 'class': 'login-input'}),
        label='새로운 비밀번호 확인',
        label_suffix='',
        required=False
    )