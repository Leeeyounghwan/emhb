from django.shortcuts import render
from .models import Package

# Create your views here.
def packages(request):
  return render(request, 'packages.html', {'items' : Package.objects.all()})