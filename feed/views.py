from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post, Profile, Comment
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic



class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login') 
    template_name = 'registration/register.html'


@login_required
def index(request):

    following_users = request.user.profile.followers.all()
    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
    

    if not posts.exists():
        posts = Post.objects.all().order_by('-created_at')[:10]
    
    context = {
        'posts': posts
    }
    return render(request, 'feed/index.html', context)


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    context = {
        'post': post
    }
    return render(request, 'feed/post_detail.html', context)

@login_required
def create_post(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        caption = request.POST.get('caption', '')
        
        if image:
            post = Post.objects.create(
                author=request.user,
                image=image,
                caption=caption
            )
            messages.success(request, 'Publicación creada exitosamente!')
            return redirect('index')
        else:
            messages.error(request, 'Debes seleccionar una imagen')
    
    return render(request, 'feed/create_post.html')

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    
    return redirect(request.META.get('HTTP_REFERER', 'index'))

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text:
            Comment.objects.create(
                post=post,
                user=request.user,
                text=text
            )
    
    return redirect(request.META.get('HTTP_REFERER', 'index'))

def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    posts = Post.objects.filter(author=user).order_by('-created_at')
    
    context = {
        'profile': profile,
        'posts': posts
    }
    return render(request, 'feed/profile.html', context)

@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    
    if request.user == user_to_follow:
        return HttpResponseForbidden("No puedes seguirte a ti mismo")
    
    profile = user_to_follow.profile
    
    if request.user in profile.followers.all():
        profile.followers.remove(request.user)
    else:
        profile.followers.add(request.user)
    
    return redirect('profile', username=username)

@login_required
def edit_profile(request):
    profile = request.user.profile
    
    if request.method == 'POST':
        bio = request.POST.get('bio', '')
        profile_picture = request.FILES.get('profile_picture')
        
        profile.bio = bio
        if profile_picture:
            profile.profile_picture = profile_picture
        profile.save()
        
        messages.success(request, 'Perfil actualizado exitosamente!')
        return redirect('profile', username=request.user.username)
    
    context = {
        'profile': profile
    }
    return render(request, 'feed/edit_profile.html', context)

