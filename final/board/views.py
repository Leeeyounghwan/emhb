from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from .models import Post, PostComment
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .forms import PostWriteForm
from django.http import JsonResponse

class BoardListView(ListView):
    model = Post
    paginate_by = 10
    template_name = "boards/board_test.html"
    context_object_name = "post_list"
    
    def get_queryset(self):
        board_list = Post.objects.order_by('-id') 
        return board_list
    
    # 페이지네이션 오버라이딩
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range

        return context

def post_detail_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.review += 1
    post.save()
    comment = PostComment.objects.filter(post_name=post)
    context = {
        'post':post,
        'comment':comment
    }
    return render(request, 'boards/post_test.html', context)

@login_required
def post_write_view(request):
    if request.method == 'POST':
        form = PostWriteForm(request.POST)
        user = request.user
        if form.is_valid():
            post = form.save(commit=False)
            post.writer = user
            post.save()
            return redirect('board:board_list')
    else:
        form = PostWriteForm()          
    return render(request, 'boards/write.html', {'form':form})

def post_update_view(request):
    return

@login_required
def post_comment_add_view(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(id=pk)
        content = request.POST.get('content')
        if len(content) <= 300 :
            obj= PostComment.objects.create(
                post_name = post,
                writer = request.user,
                content = content
            )
            context = {
                'is_create': True,
                'comment':obj            
            }
            return JsonResponse(context)
    return JsonResponse({'is_create':False})