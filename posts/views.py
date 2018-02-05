from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Post, Like
from .forms import PostForm
from .forms import UserSignup, UserLogin, UserForm, ProfileForm
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

    objects = Post.objects.filter(author=request.user)

    query = request.GET.get("q")
    if query:
        return redirect("search")

    return render(request,'home.html',{'list': objects, 'user': request.user})

def detail(request, author_id):
    user = User.objects.get(id=author_id)
    objects = Post.objects.filter(author=user)
    query = request.GET.get("q")
    if query:
        return redirect("search")

    return render(request,'detail.html',{'list': objects, 'user': user})


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
    print(query)
    if query:
        accounts = User.objects.filter(
            Q(first_name__icontains=query)|
            Q(last_name__icontains=query)
            ).distinct()
        context = {
            'users': accounts
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

def ajax_like(request, post_id):
    post = Post.objects.get(id=post_id)
    new_like, created = Like.objects.get_or_create(user=request.user, post=post)

    if created:
        action="like"
    else:
        new_like.delete()
        action="unlike"

    post_like_count = post.like_set.all().count()
    response = {
        "action": action,
        "post_like_count": post_like_count,
    }
    return JsonResponse(response, safe=False)