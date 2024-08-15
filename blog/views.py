from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import CommentForm, EmailPostForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
# Create your views here.

class PostListView(ListView):
    # model = Post
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'
    
def post_list(request):
    posts_list = Post.published.all()
    paginator = Paginator(posts_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
        
    return render(request, 'blog/post/list.html',{'posts': posts})



def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, 
                             slug=post, 
                             publish__year=year, 
                             publish__month=month, 
                             publish__day=day, 
                             status=Post.Status.PUBLISHED)
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()

    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'form': form})


def share_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}" 
            message = f"Hey {cd['name']} recommends you to read {post.title} at {post_url} \n\n {cd['name']} comments: {cd['comment']}"
            send_mail(subject=subject, message=message, from_email="maria@mail.nom", recipient_list=[cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {'form': form, 'post': post, 'sent': sent})

@require_POST
def comment_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comment = None
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    return render(request, 'blog/post/comment.html', {'form': form, 'post': post, 'comment': comment})
