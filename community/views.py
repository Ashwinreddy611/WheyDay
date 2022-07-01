from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import CommentForm, PostForm
from .models import Post, Comment
from django.contrib import messages
# Create your views here.
def community(request):
    posts = Post.objects.all()
    return render(request, 'community/community.html', {'posts': posts} )


def post_detail(request, slug):
    post = Post.objects.get(slug=slug) 

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', slug=post.slug)

    else:
        form = CommentForm()


    return render(request, 'community/post_detail.html', {'post': post,'form': form})


def add_post(request):
    if not request.user.is_superuser:
        messages.error(request,
                       'Sorry, This action is for the admin only')
        return redirect(reverse('community'))

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            form.save()
            messages.success(request, 'Successfully added Post!')
            return redirect(reverse('community'))
        else:
            messages.error(request,
                           'Could not add post to site. \
                           Please ensure form is valid!')
    else:
        form = PostForm()

    return render(request, 'community/add_post.html', {'form': form})


def edit_post(request, post_id):
    """ edits a blog post on the store """
    if not request.user.is_superuser:
        messages.error(request,
                       'Sorry, only store admin can do update a blog post')
        return redirect(reverse('community'))

    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            form.save()
            messages.success(request, 'Successfully Updated Post!')
            return redirect(reverse('community'))
        else:
            messages.error(request,
                           'Could not add post to site. \
                           Please ensure form is valid!')
    else:
        form = PostForm(instance=post)
        messages.info(request, f'You are editing {post.title}')

    return render(request, 'edit_post', {'form': form, 'post': post})