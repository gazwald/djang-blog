from django.shortcuts import render, get_object_or_404
from .models import Post


def index(request):
    posts = Post.objects.order_by('-date_pub')[:5]
    context = {'posts': posts}
    return render(request, 'posts/view.html', context)


def post_view(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {'post': post}
    return render(request, 'posts/view.html', context)


def post_add(request):
    post = get_object_or_404(Post, pk=post_id)
    context = {'post': post}
    return render(request, 'posts/view.html', context)
