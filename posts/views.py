import json
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Post, Connection, Comment
from .forms import PostForm
from .forms import UserSignup, UserLogin, UserForm, ProfileForm, CommentForm
from .serializers import CommentSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User

# Create your views here.
def usersignup(request):
    query = request.GET.get("q")
    if query:
        return redirect("search")

    context = {}
    form = UserSignup()
    context['form'] = form

    if request.method == 'POST':
        form = UserSignup(request.POST)
        if form.is_valid():
            user = form.save()
            x = user.username
            y = user.password

            user.set_password(y)
            user.save()

            auth = authenticate(username=x, password=y)
            login(request, auth)

            return redirect("profile")
        messages.warning(request, form.errors)
        return redirect("signup")
    return render(request, 'signup.html', context)


def userlogin(request):
    query = request.GET.get("q")
    if query:
        return redirect("search")

    context = {}
    form = UserLogin()
    context['form'] = form

    if request.method == 'POST':
        form = UserLogin(request.POST)
        if form.is_valid():
            user_user = form.cleaned_data['username']
            user_pass = form.cleaned_data['password']

            auth = authenticate(username=user_user, password=user_pass)
            if auth is not None:
                login(request, auth)
                return redirect("home")
            messages.warning(request, 'Incorrect user/pass...')
            return redirect("login")
        messages.warning(request, form.errors)
        return redirect("login")
    return render(request, 'login.html', context)


def userlogout(request):
    logout(request)
    return redirect("login")

def home(request):
    if not request.user.is_authenticated:
        return redirect("login")

    form = CommentForm()
    form.form_show_labels = False

    following = Connection.objects.filter(follower=request.user).count()
    followers = Connection.objects.filter(following=request.user).count()

    list = []
    posts = Post.objects.filter(author=request.user).order_by("-id")
    for post in posts:
        comments = Comment.objects.filter(post=post).order_by("timestamp")
        like_count = post.liked_by.all().count()
        check = post.liked_by.filter(id=request.user.id)
        if check:
            list.append({'post': post, 'liked': True, 'like_count': like_count, 'comments': comments})
        else:
            list.append({'post': post, 'liked': False, 'like_count': like_count, 'comments': comments})
    query = request.GET.get("q")
    if query:
        return redirect("search")
    context = {
        'list': list,
        'user': request.user,
        'form': form,
        'followers': followers,
        'following': following,
    }
    return render(request,'home.html',context)

def detail(request, author_id):
    if not request.user.is_authenticated:
        messages.warning(request, "You need to login before you can view this account")
        return redirect("login")

    myuser = request.user
    user = User.objects.get(id=author_id)
    if myuser == user:
        return redirect("home")

    following = Connection.objects.filter(follower=user).count()
    followers = Connection.objects.filter(following=user).count()


    form = CommentForm()
    list = []
    posts = Post.objects.filter(author=user).order_by("-id")
    for post in posts:
        comments = Comment.objects.filter(post=post).order_by("timestamp")
        like_count = post.liked_by.all().count()
        check = post.liked_by.filter(id=request.user.id)
        if check:
            list.append({'post': post, 'liked': True, 'like_count': like_count, 'comments': comments})
        else:
            list.append({'post': post, 'liked': False, 'like_count': like_count, 'comments': comments})
    query = request.GET.get("q")
    if query:
        return redirect("search")

    following_check = False
    if Connection.objects.filter(follower=myuser,following=user).exists():
        following_check = True

    context = {
        'list': list,
        'user': user,
        'myuser': myuser,
        'following_check': following_check,
        'form': form,
        'followers': followers,
        'following': following,
    }
    return render(request,'detail.html', context)


def create(request):
    query = request.GET.get("q")
    if query:
        return redirect("search")

    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect("home")
    context = {
    "form": form,
    }
    return render(request, 'create.html', context)

def search(request):
    query = request.GET.get("q")
    context = {
    }
    if query:
        accounts = User.objects.filter(
            Q(username__icontains=query)
            ).distinct()
        context = {
            'users': accounts,
            'nothing': False
        }
        if len(accounts) == 0:
            context = {
                'users': accounts,
                'nothing': True
            }


    return render(request, 'search.html',context)

def updateprofile(request):
    query = request.GET.get("q")
    if query:
        return redirect("search")

    if request.method == 'POST':
        user_form = UserForm(request.POST or None, request.FILES or None, instance=request.user)
        profile_form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', { 'user_form': user_form,'profile_form': profile_form})


def follow(request, author_id):
    if not request.user:
        messages.warning(request, "You need to login before you can follow people")
        return redirect("login")
    follower = User.objects.get(username=request.user)
    following = User.objects.get(id=author_id)

    if follower == following:
        messages.warning(request,'You cannot follow yourself...')

    else:
        _, created = Connection.objects.get_or_create(follower=follower,following=following)

        if created:
            messages.success(request, "You are now following "+following.username)
    return redirect("/account/"+str(author_id))

def unfollow(request, author_id):
    follower = User.objects.get(username=request.user)
    following = User.objects.get(id=author_id)

    if follower == following:
        messages.warning(request,'You cannot follow yourself...')
        return redirect("/account/" + str(author_id))
    else:
        unfollow = Connection.objects.get(
            follower=follower,
            following=following
        )

    if unfollow:
        unfollow.delete()
        messages.success(request, "You are now unfollowing " + following.username)

    return redirect("home")

def feed(request):
    if not request.user.is_authenticated:
        return redirect("login")
    following = Connection.objects.filter(follower=request.user)
    posts = Post.objects.all().order_by("-id")
    feed = []
    form = CommentForm()
    for post in posts:
        for account in following:
            if post.author == account.following:
                feed.append(post)
    list = []
    for post in feed:
        comments = Comment.objects.filter(post=post).order_by("timestamp")
        like_count = post.liked_by.all().count()
        check = post.liked_by.filter(id=request.user.id)
        if check:
            list.append({'post': post, 'liked': True, 'like_count': like_count, 'comments': comments})
        else:
            list.append({'post': post, 'liked': False, 'like_count': like_count, 'comments': comments})
    context = {
        'feed': list,
        'form': form,
    }
    return render(request, 'feed.html', context)

def ajax_like(request, post_id):
    post = Post.objects.get(id=post_id)
    try:
        post.liked_by.get(id=request.user.id)
        post.liked_by.remove(request.user)
        created = False
    except:
        post.liked_by.add(request.user)
        created = True

    if created:
        action="like"
    else:
        action="unlike"

    post_like_count = post.liked_by.all().count()
    response = {
        "action": action,
        "post_like_count": post_like_count,
    }
    return JsonResponse(response, safe=False)


def comment(request, post_id, page):
    instance = Post.objects.get(id=post_id)
    user = User.objects.get(username=instance.author)
    if request.method == "POST":
         form = CommentForm(request.POST)
         if form.is_valid():
             comment = form.save(commit=False)
             comment.post = instance
             comment.user = request.user
             comment.save()
             if page == 'detail':
                return redirect("/account/" + str(user.id))
             else:
                return redirect("feed")



def followinglist(request, author_id):
    user = User.objects.get(id=author_id)
    following = Connection.objects.filter(follower=user).order_by("-id")
    accounts = []
    for account in following:
        if user == request.user:
            accounts.append({'user': account.following, 'following': True})
        elif account.following == request.user:
            accounts.append({'user': account.following, 'following': False})
        elif Connection.objects.filter(follower=request.user,following=account.following):
            accounts.append({'user': account.following, 'following': True})
        else:
            accounts.append({'user': account.following, 'following': False})

    return render(request, 'list.html', {'accounts':accounts})

def followerslist(request, author_id):
    user = User.objects.get(id=author_id)
    followers = Connection.objects.filter(following=user).order_by("-id")
    accounts = []
    for account in followers:
        if account.following == request.user:
            accounts.append({'user': account.follower, 'following': False})
        elif Connection.objects.filter(follower=request.user,following=account.follower):
            accounts.append({'user': account.follower, 'following': True})
        else:
            accounts.append({'user': account.follower, 'following': False})

    return render(request, 'list.html', {'accounts':accounts})


