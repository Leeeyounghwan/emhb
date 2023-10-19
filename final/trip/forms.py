from django import forms
from .models import Package
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class Package(forms.ModelForm):
  class Meta:
    model = Package
    exclude = ['created_at','updated_at']
    fields = ['destination', 'title', 'price', 'image', 'content', 'start_date', 'end_date', 'created_at', 'updated_at']

class UserForm(UserCreationForm):

  class Meta:
    model = User
    fields= ('username', 'password1', 'password2')
