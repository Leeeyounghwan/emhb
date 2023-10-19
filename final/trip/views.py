from django.shortcuts import render
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
import openai
import json
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

# chatbot 테스트 

def chatapi(request, question):
    with open('../config.json', 'r') as f:
        json_data = json.load(f)
    api_key = json_data['OPENAI_KEY']
                
    response_generator = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {
            "role": "system",
            "content": "너는 우리 트립웹에 Trip봇이야."},
            {"role": "user", "content": f"'{question}'에 대해서 친절히 답변해줘"},
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