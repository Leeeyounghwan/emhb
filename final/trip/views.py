from django.shortcuts import render, redirect, get_object_or_404
from .models import Package, User, Report
from django.contrib.auth.decorators import login_required
import openai
from django.http import JsonResponse
import json


# Create your views here.

#마이페이지 by 준경
def mypage(request):
    return render(request, 'mypage.html')
def charts(request):
    return render(request,'charts.html')

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

    # if admin_check(request) == True :
    return render(request, "admin/create_product.html")
    # else:
    #     return redirect("trip:main")

def product_management(request):

    packages = Package.objects.all()
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

def order_inquiry(request):
    return render(request, "admin/order_inquiry.html")

def delivery_tracking(request):
    return render(request, "admin/delivery_tracking.html")

def return_management(request):
    return render(request, "admin/return_management.html")

def report_detail(request):

    if admin_check(request) == True :
        reports = Report.objects.all()
        context = {
            "reports" : reports
        }

        return render(request, "admin/report_detail.html", context)
    else:
        return redirect("trip:main")

def user_management(request):

    if admin_check(request) == True :
        users = User.objects.all()
        context = {
            "users" : users
        }

        return render(request, "admin/user_management.html", context)
    else:
        return redirect("trip:main")

def blacklist_management(request):

    if admin_check(request) == True :
        blacklist = User.objects.filter(is_black=True)
        context = {
            "blacklist" : blacklist
        }

        return render(request, "admin/blacklist_management.html", context)
    else:
        return redirect("trip:main")


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


# 챗봇 BY 영민
def chatapi(request, question):
    with open('../config.json', 'r') as f:
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