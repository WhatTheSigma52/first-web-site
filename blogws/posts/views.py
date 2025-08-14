from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm, ProfileForm
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator

from .models import Group, Post, Comment, Subscribe


User = get_user_model()


ITEMS_PER_PAGE = 3


def get_pagination(request, group):
    paginator = Paginator(group, ITEMS_PER_PAGE)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    return page_obj


def index(request):
    posts = Post.objects.select_related('group', 'author')
    page_obj = get_pagination(request, posts)
    context = {'posts': posts, 'page_obj': page_obj}
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.select_related('author')
    page_obj = get_pagination(request, posts)
    context = {'group': group, 'posts': posts, 'page_obj': page_obj}
    return render(request, 'posts/group_list.html', context)


@login_required
def make_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author_id = request.user.id
        post.save()
        return redirect('posts:index')
    context = {'form': form}
    return render(request, 'posts/post_create.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.select_related('group')
    page_obj = get_pagination(request, posts)
    posts_count = posts.count()
    user = request.user
    following = (
        user.is_authenticated and author.following.filter(
            subscriber=user, author=author).exists() and user.follower.filter(
                subscriber=user, author=author).exists())
    profile = author.profile
    context = {'author': author,
               'page_obj': page_obj,
               'posts_count': posts_count,
               'following': following,
               'user': user,
               'profile': profile}
    return render(request, 'posts/profile.html', context)


def post_page(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    posts_count = post.author.posts.count()
    comments = post.comments.all()
    form = CommentForm()
    context = {'post': post,
               'posts_count': posts_count,
               'comments': comments,
               'form': form}
    return render(request, 'posts/post_details.html', context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        return redirect('posts:post_detail', post_id=post_id)
    form = PostForm(request.POST or None,
                    instance=post,
                    files=request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)
    context = {'form': form, 'post': post, 'is_edit': True}
    return render(request, 'posts/post_create.html', context)


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    username = post.author.get_username()
    if request.user != post.author:
        return redirect('posts:post_detail', post_id=post_id)
    post.delete()
    return redirect('posts:profile', username=username)


@login_required
def comment_create(request, post_id):
    form = CommentForm(request.POST or None)
    post = get_object_or_404(Post, pk=post_id)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author_id = request.user.id
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        return redirect('posts:post_detail', post_id=comment.post.id)
    comment.delete()
    return redirect('posts:post_detail', post_id=comment.post.id)


@login_required
def subscribe(request, username):
    author = get_object_or_404(User, username=username)
    user = request.user
    if user != author:
        sub = Subscribe.objects.get_or_create(subscriber=user, author=author)
    return redirect('posts:profile', username=username)


@login_required
def unsubscribe(request, username):
    author = get_object_or_404(User, username=username)
    user = request.user
    unsub = Subscribe.objects.get(subscriber=user, author=author)
    unsub.delete()
    return redirect('posts:profile', username=username)


@login_required
def favourite(request):
    posts = Post.objects.filter(author__following__subscriber=request.user)
    page_obj = get_pagination(request, posts)
    context = {'page_obj': page_obj}
    return render(request, 'posts/favourite.html', context)


@login_required
def edit_profile(request, username):
    author = get_object_or_404(User, username=username)
    profile = author.profile
    form = ProfileForm(request.POST or None,
                       instance=profile,
                       files=request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('posts:profile', username=username)
    context = {'author': author,
               'profile': profile,
               'form': form}
    return render(request, 'posts/edit_profile.html', context)
