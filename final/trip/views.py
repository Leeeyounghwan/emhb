from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from .models import TogetherPost,TogetherComment
from .forms import CommentForm
from django.utils import timezone

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
    post = get_object_or_404(TogetherPost)
    return render(request, 'single-blog.html',{'post':post})

def together_comment(request, post_id):
    post = TogetherPost.objects.get(pk=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            return redirect('view_post', post_id=post_id)
    else:
        form = CommentForm()

    return render(request, 'single-blog.html', {'form': form})

#by 건영 종료