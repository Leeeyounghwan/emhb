from django import forms
from .models import Package

class Package(forms.ModelForm):
  class Meta:
    model = Package
    fields = ['destination', 'title', 'price', 'image', 'content', 'start_date', 'end_date', 'created_at', 'updated_at']